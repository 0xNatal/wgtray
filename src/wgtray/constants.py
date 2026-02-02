"""Constants and paths for wgtray."""

from pathlib import Path

VERSION = "1.4.0"

def find_libdir():
    system_path = Path("/usr/share/wgtray/lib")
    return system_path if system_path.exists() else Path(__file__).parent.parent / "lib"

def find_icondir():
    system_path = Path("/usr/share/icons/hicolor/scalable/apps")
    if (system_path / "wgtray.svg").exists():
        return system_path
    return Path(__file__).parent.parent.parent / "res" / "icons"

LIBDIR = find_libdir()
ICONDIR = find_icondir()
CONFIG_DIR = Path.home() / ".config" / "wgtray"
CONFIG_FILE = CONFIG_DIR / "config.toml"
HOOKS_DIR = CONFIG_DIR / "hooks"
AUTOSTART_FILE = Path.home() / ".config" / "autostart" / "wgtray.desktop"
SYSTEM_DESKTOP = Path("/usr/share/applications/wgtray.desktop")

ICONS = {
    "disconnected": {
        "dark": "wgtray.svg",
        "light": "wgtray-light.svg",
    },
    "connected": {
        "dark": "wgtray-connected.svg",
        "light": "wgtray-connected-light.svg",
    },
}

DEFAULT_CONFIG = {
    "notifications": True,
    "autoconnect": False,
    "default_connection": "",
    "last_connection": "",
    "icon_theme": "auto",
    "monitor_mode": "auto",
    "poll_interval": 5000,
    "require_password": True,
}