"""Main application class for wgtray."""

import sys
import time
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox, QDialog
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

from .constants import VERSION, ICONDIR, ICONS
from .config import load_config, save_config
from .monitor import NetlinkMonitor
from .settings import SettingsDialog
from .logger import setup_logging, logger
from .wireguard import (
    get_active_connections, get_configs, connect, disconnect,
    check_config_dir_permissions, open_config_folder,
    get_connection_stats, format_bytes, format_handshake
)


def detect_system_theme():
    """Detect if system uses light or dark theme."""
    try:
        app = QApplication.instance()
        if app:
            palette = app.palette()
            bg = palette.window().color()
            is_dark_bg = bg.lightness() < 128
            return "light" if is_dark_bg else "dark"
    except Exception:
        pass
    return "dark"


def get_icon(name, theme="auto"):
    """Get icon by name, respecting theme."""
    if theme == "auto":
        theme = detect_system_theme()

    icon_variants = ICONS.get(name, ICONS["disconnected"])
    icon_file = icon_variants.get(theme, icon_variants.get("dark"))
    icon_path = ICONDIR / icon_file

    if not icon_path.exists() and theme == "light":
        icon_file = icon_variants.get("dark")
        icon_path = ICONDIR / icon_file

    if icon_path.exists():
        return QIcon(str(icon_path))

    print(f"Warning: Icon not found: {icon_path}", file=sys.stderr)
    return QIcon()


class WgTray:
    def __init__(self, debug: bool = False):
        self._debug = debug
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("wgtray")
        self.app.setDesktopFileName("wgtray")

        self._config = load_config()

        setup_logging(debug=self._debug)
        logger.info(f"wgtray {VERSION} starting")

        check_config_dir_permissions()

        self._cache_active = []
        self._cache_configs = []
        self._cache_time = 0
        self._cache_ttl = 2
        self._last_state = None

        self.menu = QMenu()
        self.tray = QSystemTrayIcon()
        self.tray.setContextMenu(self.menu)
        self.menu.aboutToShow.connect(self.build_menu)
        self.tray.activated.connect(self.on_tray_click)

        self._setup_monitoring()

        self.update_icon()
        self.build_menu()
        self.tray.setVisible(True)

        if self._config.get("autoconnect", False):
            QTimer.singleShot(1000, self._auto_connect)

    def _setup_monitoring(self):
        """Setup network monitoring based on config."""
        mode = self._config.get("monitor_mode", "auto")

        self.netlink = None
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.poll_check)

        use_netlink = False
        if mode in ("auto", "netlink"):
            self.netlink = NetlinkMonitor()
            if self.netlink.available:
                use_netlink = True
                self.netlink.changed.connect(self.on_network_change)
                self.netlink.start()

        if mode == "netlink" and not use_netlink:
            print("Warning: Netlink requested but not available, falling back to polling", file=sys.stderr)

        interval = self._config.get("poll_interval", 3000)
        self.poll_timer.start(interval)

        self._monitor_mode = "netlink" if use_netlink else "polling"
        logger.info(f"Monitor mode: {self._monitor_mode}")

    def _auto_connect(self):
        """Auto-connect to default or last VPN."""
        active = get_active_connections()
        if active:
            return

        configs = get_configs()
        if not configs:
            return

        default = self._config.get("default_connection") or self._config.get("last_connection")
        if default and default in configs:
            self.on_connect(default)
        elif configs:
            self.on_connect(configs[0])

    def poll_check(self):
        active = get_active_connections()
        state = tuple(sorted(active))
        if state != self._last_state:
            self._last_state = state
            self.update_icon()
        elif active:
            self._update_tooltip(active)

    def on_network_change(self):
        QTimer.singleShot(300, self.update_icon)

    def _refresh_cache(self, force=False):
        now = time.time()
        if force or (now - self._cache_time > self._cache_ttl):
            self._cache_active = get_active_connections()
            self._cache_configs = get_configs()
            self._cache_time = now

    def show_notification(self, title, message, error=False):
        if not self._config.get("notifications", True):
            return
        icon = QSystemTrayIcon.MessageIcon.Critical if error else QSystemTrayIcon.MessageIcon.Information
        self.tray.showMessage(title, message, icon, 3000)

    def _update_tooltip(self, active):
        """Update tooltip with connection stats."""
        if active:
            tooltip_lines = ["WireGuard: Connected"]
            for iface in active:
                stats = get_connection_stats(iface)
                if stats:
                    rx = format_bytes(stats["rx_bytes"])
                    tx = format_bytes(stats["tx_bytes"])
                    hs = format_handshake(stats["latest_handshake"])
                    tooltip_lines.append(f"{iface}: ↓{rx} ↑{tx} ({hs})")
                else:
                    tooltip_lines.append(iface)
            self.tray.setToolTip("\n".join(tooltip_lines))
        else:
            self.tray.setToolTip("WireGuard: Not connected")

    def update_icon(self):
        self._refresh_cache(force=True)
        active = self._cache_active
        self._last_state = tuple(sorted(active))

        theme = self._config.get("icon_theme", "auto")

        if active:
            self.tray.setIcon(get_icon("connected", theme))
        else:
            self.tray.setIcon(get_icon("disconnected", theme))

        self.app.setWindowIcon(get_icon("disconnected", theme))
        self._update_tooltip(active)

    def build_menu(self):
        self.menu.clear()
        self._refresh_cache()

        active = self._cache_active
        configs = self._cache_configs

        status_text = f"Connected ({', '.join(active)})" if active else "Not connected"
        status = QAction(f"Status: {status_text}", self.menu)
        status.setEnabled(False)
        self.menu.addAction(status)
        self.menu.addSeparator()

        if configs:
            for name in configs:
                if name in active:
                    action = QAction(f"✓ {name}", self.menu)
                    action.triggered.connect(lambda c, n=name: self.on_disconnect(n))
                else:
                    action = QAction(f"   {name}", self.menu)
                    action.triggered.connect(lambda c, n=name: self.on_connect(n))
                self.menu.addAction(action)
        else:
            no_conf = QAction("No configurations found", self.menu)
            no_conf.setEnabled(False)
            self.menu.addAction(no_conf)

        self.menu.addSeparator()

        folder = QAction("Open config folder", self.menu)
        folder.triggered.connect(open_config_folder)
        self.menu.addAction(folder)

        self.menu.addSeparator()

        settings = QAction("Settings", self.menu)
        settings.triggered.connect(self.on_settings)
        self.menu.addAction(settings)

        self.menu.addSeparator()

        quit_action = QAction("Quit", self.menu)
        quit_action.triggered.connect(self.quit)
        self.menu.addAction(quit_action)

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            active = get_active_connections()
            if active:
                self.on_disconnect(active[0])
            else:
                configs = get_configs()
                if not configs:
                    return
                default = self._config.get("default_connection") or self._config.get("last_connection")
                if default and default in configs:
                    self.on_connect(default)
                elif configs:
                    self.on_connect(configs[0])

    def on_connect(self, name):
        active = get_active_connections()
        if name in active:
            self.show_notification("WireGuard", f"Already connected to {name}")
            return

        for conn in active:
            disconnect(conn, require_password=False)

        logger.info(f"Connecting to {name}")
        require_pw = self._config.get("require_password", True)
        success, hook_error, cancelled = connect(name, require_password=require_pw)

        if cancelled:
            return

        if success:
            logger.info(f"Connected to {name}")
            msg = f"Connected to {name}"
            if hook_error:
                msg += f"\n⚠ Hook failed: {hook_error}"
            self.show_notification("WireGuard", msg, error=bool(hook_error))
            self._config["last_connection"] = name
            save_config(self._config)
        else:
            logger.error(f"Failed to connect to {name}")
            self.show_notification("WireGuard", f"Failed to connect to {name}", error=True)
        self.update_icon()

    def on_disconnect(self, name):
        logger.info(f"Disconnecting from {name}")
        require_pw = self._config.get("require_password", True)
        success, hook_error, cancelled = disconnect(name, require_password=require_pw)

        if cancelled:
            return

        if success:
            logger.info(f"Disconnected from {name}")
            msg = f"Disconnected from {name}"
            if hook_error:
                msg += f"\n⚠ Hook failed: {hook_error}"
            self.show_notification("WireGuard", msg, error=bool(hook_error))
        else:
            logger.error(f"Failed to disconnect from {name}")
            self.show_notification("WireGuard", f"Failed to disconnect from {name}", error=True)
        self.update_icon()

    def on_refresh(self):
        self._refresh_cache(force=True)
        self.update_icon()

    def on_settings(self):
        dialog = SettingsDialog(self._config, self._cache_configs, self._monitor_mode)
        dialog.refresh_clicked.connect(self.on_refresh)
        dialog.about_clicked.connect(self.on_about)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            old_mode = self._config.get("monitor_mode")
            old_interval = self._config.get("poll_interval")

            self._config = dialog.get_config()
            save_config(self._config)
            logger.info("Settings saved")

            if (self._config.get("monitor_mode") != old_mode or
                self._config.get("poll_interval") != old_interval):
                self._restart_monitoring()

            self.update_icon()

    def _restart_monitoring(self):
        """Restart monitoring with new settings."""
        if self.netlink:
            self.netlink.stop()
        self.poll_timer.stop()
        self._setup_monitoring()

    def on_about(self):
        QMessageBox.about(
            None,
            "About wgtray",
            f"<h3>wgtray</h3>"
            f"<p>Version {VERSION}</p>"
            f"<p>A lightweight WireGuard system tray client for Linux.</p>"
            f"<p><a href='https://github.com/0xNatal/wgtray'>github.com/0xNatal/wgtray</a></p>"
            f"<p>License: GPL-3.0</p>"
        )

    def quit(self):
        logger.info("wgtray shutting down")
        if self.netlink:
            self.netlink.stop()
        self.poll_timer.stop()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())