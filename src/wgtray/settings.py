"""Settings dialog for wgtray."""

from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QComboBox, QPushButton, QGroupBox,
    QSpinBox, QStyle
)
from PyQt6.QtCore import Qt, pyqtSignal
from .config import is_autostart_enabled, set_autostart
from .constants import HOOKS_DIR
from .logger import get_log_path


class SettingsDialog(QDialog):
    refresh_clicked = pyqtSignal()
    about_clicked = pyqtSignal()

    def __init__(self, config, configs_list, monitor_mode="unknown", parent=None):
        super().__init__(parent)
        self.config = config.copy()
        self.configs_list = configs_list
        self.monitor_mode = monitor_mode

        self.setWindowTitle("wgtray Settings")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # === General ===
        general_group = QGroupBox("General")
        general_layout = QVBoxLayout(general_group)

        self.autostart_cb = QCheckBox("Start on login")
        self.autostart_cb.setChecked(is_autostart_enabled())
        general_layout.addWidget(self.autostart_cb)

        self.notifications_cb = QCheckBox("Show notifications")
        self.notifications_cb.setChecked(self.config.get("notifications", True))
        general_layout.addWidget(self.notifications_cb)

        layout.addWidget(general_group)

        # === Connection ===
        conn_group = QGroupBox("Connection")
        conn_layout = QVBoxLayout(conn_group)

        self.autoconnect_cb = QCheckBox("Auto-connect on start")
        self.autoconnect_cb.setChecked(self.config.get("autoconnect", False))
        conn_layout.addWidget(self.autoconnect_cb)

        default_layout = QHBoxLayout()
        default_layout.addWidget(QLabel("Default VPN:"))
        self.default_combo = QComboBox()
        self.default_combo.addItem("(Last used)", "")
        for cfg in self.configs_list:
            self.default_combo.addItem(cfg, cfg)
        idx = self.default_combo.findData(self.config.get("default_connection", ""))
        if idx >= 0:
            self.default_combo.setCurrentIndex(idx)
        default_layout.addWidget(self.default_combo, 1)
        conn_layout.addLayout(default_layout)

        layout.addWidget(conn_group)

        # === Appearance ===
        appear_group = QGroupBox("Appearance")
        appear_layout = QVBoxLayout(appear_group)

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Icon theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Auto", "auto")
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("Light", "light")
        idx = self.theme_combo.findData(self.config.get("icon_theme", "auto"))
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        theme_layout.addWidget(self.theme_combo, 1)
        appear_layout.addLayout(theme_layout)

        layout.addWidget(appear_group)

        # === Advanced ===
        adv_group = QGroupBox("Advanced")
        adv_layout = QVBoxLayout(adv_group)

        monitor_layout = QHBoxLayout()
        monitor_layout.addWidget(QLabel("Monitor mode:"))
        self.monitor_combo = QComboBox()
        self.monitor_combo.addItem("Auto", "auto")
        self.monitor_combo.addItem("Netlink", "netlink")
        self.monitor_combo.addItem("Polling", "polling")
        idx = self.monitor_combo.findData(self.config.get("monitor_mode", "auto"))
        if idx >= 0:
            self.monitor_combo.setCurrentIndex(idx)
        monitor_layout.addWidget(self.monitor_combo, 1)
        adv_layout.addLayout(monitor_layout)

        poll_layout = QHBoxLayout()
        poll_layout.addWidget(QLabel("Poll interval:"))
        self.poll_spin = QSpinBox()
        self.poll_spin.setRange(1, 60)
        self.poll_spin.setSuffix(" sec")
        self.poll_spin.setValue(self.config.get("poll_interval", 3000) // 1000)
        poll_layout.addWidget(self.poll_spin)
        poll_layout.addStretch()
        adv_layout.addLayout(poll_layout)

        layout.addWidget(adv_group)

        # === Info ===
        info_group = QGroupBox("Info")
        info_layout = QVBoxLayout(info_group)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Active monitor:"))
        mode_layout.addWidget(QLabel(f"<b>{self.monitor_mode.capitalize()}</b>"))
        mode_layout.addStretch()
        info_layout.addLayout(mode_layout)

        log_layout = QHBoxLayout()
        log_layout.addWidget(QLabel("Log file:"))
        log_path = QLabel(f"<a href='file://{get_log_path()}'>{get_log_path()}</a>")
        log_path.setOpenExternalLinks(True)
        log_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        log_layout.addWidget(log_path, 1)
        info_layout.addLayout(log_layout)

        hooks_layout = QHBoxLayout()
        hooks_layout.addWidget(QLabel("Hooks folder:"))
        hooks_display = str(HOOKS_DIR).replace(str(Path.home()), "~")
        hooks_path = QLabel(f"<a href='file://{HOOKS_DIR}'>{hooks_display}</a>")
        hooks_path.setOpenExternalLinks(True)
        hooks_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        hooks_layout.addWidget(hooks_path, 1)
        info_layout.addLayout(hooks_layout)

        layout.addWidget(info_group)

        # === Buttons ===
        layout.addStretch()
        btn_layout = QHBoxLayout()

        about_btn = QPushButton()
        about_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation))
        about_btn.setToolTip("About")
        about_btn.clicked.connect(self.about_clicked.emit)
        btn_layout.addWidget(about_btn)

        refresh_btn = QPushButton()
        refresh_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        refresh_btn.setToolTip("Refresh")
        refresh_btn.clicked.connect(self.refresh_clicked.emit)
        btn_layout.addWidget(refresh_btn)

        btn_layout.addStretch()

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setDefault(True)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def get_config(self):
        """Return updated config after dialog accepted."""
        set_autostart(self.autostart_cb.isChecked())

        return {
            **self.config,
            "notifications": self.notifications_cb.isChecked(),
            "autoconnect": self.autoconnect_cb.isChecked(),
            "default_connection": self.default_combo.currentData(),
            "icon_theme": self.theme_combo.currentData(),
            "monitor_mode": self.monitor_combo.currentData(),
            "poll_interval": self.poll_spin.value() * 1000,
        }