"""Constants and paths for wgtray."""

from pathlib import Path


def _load_constants():
    """Load constants from conf file."""
    conf_path = Path("/usr/share/wgtray/constants.conf")
    if not conf_path.exists():
        conf_path = Path(__file__).parent.parent.parent / "res" / "constants.conf"
    
    constants = {}
    with open(conf_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                constants[key] = value
    return constants


_CONF = _load_constants()

VERSION = _CONF["VERSION"]
HOOKS_DIR = Path(_CONF["HOOKS_DIR"])
SUDOERS_DIR = Path(_CONF["SUDOERS_DIR"])
EVENTS = _CONF["EVENTS"].split(",")


def find_libdir():
    system_path = Path("/usr/lib/wgtray")
    return system_path if system_path.exists() else Path(__file__).parent.parent.parent / "src" / "lib"


def find_icondir():
    system_path = Path("/usr/share/icons/hicolor/scalable/apps")
    if (system_path / "wgtray.svg").exists():
        return system_path
    return Path(__file__).parent.parent.parent / "res" / "icons"


LIBDIR = find_libdir()
ICONDIR = find_icondir()
CONFIG_DIR = Path.home() / ".config" / "wgtray"
CONFIG_FILE = CONFIG_DIR / "config.toml"
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