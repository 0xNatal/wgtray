"""Constants and paths for wgtray."""

from pathlib import Path

VERSION = "1.2.0"

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
CONFIG_FILE = Path.home() / ".config" / "wgtray" / "config.json"
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
    "icon_theme": "auto",  # auto, light, dark
    "monitor_mode": "auto",  # auto, netlink, polling
    "poll_interval": 3000,  # ms
}