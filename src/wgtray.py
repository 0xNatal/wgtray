#!/usr/bin/env python3
"""wgtray – a lightweight third-party WireGuard tray client"""

import sys
import signal
import subprocess
import os
import time
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer

# PyQt blocks SIGINT by default
signal.signal(signal.SIGINT, signal.SIG_DFL)


def find_libdir():
    system_path = Path("/usr/share/wgtray/lib")
    if system_path.exists():
        return system_path
    return Path(__file__).parent / "lib"  # Dev fallback


def find_icondir():
    system_path = Path("/usr/share/icons/hicolor/scalable/apps")
    if (system_path / "wgtray.svg").exists():
        return system_path
    return Path(__file__).parent.parent / "res" / "icons"  # Dev fallback


LIBDIR = find_libdir()
ICONDIR = find_icondir()

ICONS = {
    "tray-disconnected": "wgtray.svg",
    "tray-connected": "wgtray-connected.svg",
    "status-disconnected": "wgtray-status-disconnected.svg",
    "status-connected": "wgtray-status-connected.svg",
    "vpn-inactive": "wgtray-vpn-inactive.svg",
    "vpn-active": "wgtray-vpn-active.svg",
    "disconnect": "wgtray-disconnect.svg",
    "folder": "wgtray-folder.svg",
    "refresh": "wgtray-refresh.svg",
    "quit": "wgtray-quit.svg",
}


def get_icon(name):
    if name in ICONS:
        icon_path = ICONDIR / ICONS[name]
        if icon_path.exists():
            return QIcon(str(icon_path))
    return QIcon()


def run_script(script_name, *args, use_pkexec=False):
    """Run a helper script, optionally with pkexec for root privileges."""
    script_path = LIBDIR / script_name

    if not script_path.exists():
        print(f"Error: {script_path} not found", file=sys.stderr)
        return None, 1

    cmd = ["pkexec", str(script_path)] if use_pkexec else [str(script_path)]
    cmd.extend(args)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "Timeout", 1
    except Exception as e:
        return str(e), 1


def get_active_connections():
    output, code = run_script("status.sh")
    if code == 0 and output:
        return [x for x in output.split("\n") if x]
    return []


def get_configs():
    output, code = run_script("list-configs.sh")
    if code == 0 and output:
        return [x for x in output.split("\n") if x]
    return []


def connect(name):
    output, code = run_script("connect.sh", name, use_pkexec=True)
    if output:
        print(output)
    return code == 0


def disconnect(name=None):
    if name:
        output, code = run_script("disconnect.sh", name, use_pkexec=True)
    else:
        output, code = run_script("disconnect.sh", use_pkexec=True)
    if output:
        print(output)
    return code == 0


def open_config_folder():
    config_dir = os.environ.get("WG_TRAY_CONFIG_DIR", "/etc/wireguard")
    subprocess.run(["xdg-open", config_dir], check=False)


class WgTray:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("wgtray")

        self.menu = QMenu()
        self.tray = QSystemTrayIcon()
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)

        self.menu.aboutToShow.connect(self.build_menu)

        self._cache_active = []
        self._cache_configs = []
        self._cache_time = 0
        self._cache_ttl = 2  # Avoid repeated subprocess calls on rapid menu opens

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_icon)
        self.timer.start(30000)

        self.update_icon()
        self.build_menu()

    def _refresh_cache(self, force=False):
        now = time.time()
        if force or (now - self._cache_time > self._cache_ttl):
            self._cache_active = get_active_connections()
            self._cache_configs = get_configs()
            self._cache_time = now

    def show_notification(self, title, message, error=False):
        icon = QSystemTrayIcon.MessageIcon.Critical if error else QSystemTrayIcon.MessageIcon.Information
        self.tray.showMessage(title, message, icon, 3000)

    def update_icon(self):
        self._refresh_cache(force=True)
        active = self._cache_active

        if active:
            self.tray.setIcon(get_icon("tray-connected"))
            self.tray.setToolTip(f"WireGuard: {', '.join(active)}")
        else:
            self.tray.setIcon(get_icon("tray-disconnected"))
            self.tray.setToolTip("WireGuard: Not connected")

    def build_menu(self):
        self.menu.clear()
        self._refresh_cache()

        active = self._cache_active
        configs = self._cache_configs

        if active:
            status = QAction(get_icon("status-connected"), f"Connected: {', '.join(active)}", self.menu)
        else:
            status = QAction(get_icon("status-disconnected"), "Not connected", self.menu)
        status.setEnabled(False)
        self.menu.addAction(status)
        self.menu.addSeparator()

        if configs:
            for name in configs:
                if name in active:
                    action = QAction(get_icon("vpn-active"), name, self.menu)
                    action.triggered.connect(lambda checked, n=name: self.on_disconnect(n))
                else:
                    action = QAction(get_icon("vpn-inactive"), name, self.menu)
                    action.triggered.connect(lambda checked, n=name: self.on_connect(n))
                self.menu.addAction(action)
        else:
            no_conf = QAction("No configurations found", self.menu)
            no_conf.setEnabled(False)
            self.menu.addAction(no_conf)

        self.menu.addSeparator()

        if active:
            disc_action = QAction(get_icon("disconnect"), "Disconnect", self.menu)
            disc_action.triggered.connect(self.on_disconnect_all)
            self.menu.addAction(disc_action)
            self.menu.addSeparator()

        folder_action = QAction(get_icon("folder"), "Open config folder", self.menu)
        folder_action.triggered.connect(open_config_folder)
        self.menu.addAction(folder_action)

        refresh_action = QAction(get_icon("refresh"), "Refresh", self.menu)
        refresh_action.triggered.connect(self.on_refresh)
        self.menu.addAction(refresh_action)

        self.menu.addSeparator()

        quit_action = QAction(get_icon("quit"), "Quit", self.menu)
        quit_action.triggered.connect(self.app.quit)
        self.menu.addAction(quit_action)

    def on_connect(self, name):
        active = get_active_connections()

        if name in active:
            self.show_notification("WireGuard", f"Already connected to {name}")
            return

        # Disconnect others first (only one connection at a time)
        for conn in active:
            disconnect(conn)

        if connect(name):
            self.show_notification("WireGuard", f"Connected to {name}")
        else:
            self.show_notification("WireGuard", f"Failed to connect to {name}", error=True)

        self.update_icon()

    def on_disconnect(self, name):
        if disconnect(name):
            self.show_notification("WireGuard", f"Disconnected from {name}")
        else:
            self.show_notification("WireGuard", f"Failed to disconnect from {name}", error=True)
        self.update_icon()

    def on_disconnect_all(self):
        if disconnect():
            self.show_notification("WireGuard", "All connections closed")
        else:
            self.show_notification("WireGuard", "Failed to disconnect", error=True)
        self.update_icon()

    def on_refresh(self):
        self._refresh_cache(force=True)
        self.update_icon()
        self.build_menu()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    WgTray().run()