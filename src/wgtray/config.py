"""Configuration management for wgtray."""

import json
import subprocess
import tomlkit

from .constants import CONFIG_DIR, CONFIG_FILE, LIBDIR, DEFAULT_CONFIG

CONFIG_FILE_JSON = CONFIG_DIR / "config.json"


def _migrate_from_json():
    """Migrate old JSON config to TOML."""
    if CONFIG_FILE_JSON.exists() and not CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE_JSON, "r") as f:
                old_config = json.load(f)
            save_config(old_config)
            CONFIG_FILE_JSON.rename(CONFIG_FILE_JSON.with_suffix(".json.bak"))
        except Exception:
            pass


def load_config():
    """Load config from TOML file."""
    _migrate_from_json()
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                doc = tomlkit.load(f)
            return {
                "notifications": doc.get("general", {}).get("notifications", DEFAULT_CONFIG["notifications"]),
                "autoconnect": doc.get("general", {}).get("autoconnect", DEFAULT_CONFIG["autoconnect"]),
                "require_password": doc.get("general", {}).get("require_password", DEFAULT_CONFIG["require_password"]),
                "default_connection": doc.get("connection", {}).get("default", DEFAULT_CONFIG["default_connection"]),
                "last_connection": doc.get("connection", {}).get("last", DEFAULT_CONFIG["last_connection"]),
                "icon_theme": doc.get("appearance", {}).get("icon_theme", DEFAULT_CONFIG["icon_theme"]),
                "monitor_mode": doc.get("advanced", {}).get("monitor_mode", DEFAULT_CONFIG["monitor_mode"]),
                "poll_interval": doc.get("advanced", {}).get("poll_interval", DEFAULT_CONFIG["poll_interval"]),
            }
        except Exception:
            pass
    
    config = DEFAULT_CONFIG.copy()
    save_config(config)
    return config


def save_config(config):
    """Save config to TOML file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    doc = tomlkit.document()
    
    general = tomlkit.table()
    general["notifications"] = config.get("notifications", DEFAULT_CONFIG["notifications"])
    general["autoconnect"] = config.get("autoconnect", DEFAULT_CONFIG["autoconnect"])
    general["require_password"] = config.get("require_password", DEFAULT_CONFIG["require_password"])
    doc["general"] = general
    
    connection = tomlkit.table()
    connection["default"] = config.get("default_connection", DEFAULT_CONFIG["default_connection"])
    connection["last"] = config.get("last_connection", DEFAULT_CONFIG["last_connection"])
    doc["connection"] = connection
    
    appearance = tomlkit.table()
    appearance["icon_theme"] = config.get("icon_theme", DEFAULT_CONFIG["icon_theme"])
    doc["appearance"] = appearance
    
    advanced = tomlkit.table()
    advanced["monitor_mode"] = config.get("monitor_mode", DEFAULT_CONFIG["monitor_mode"])
    advanced["poll_interval"] = config.get("poll_interval", DEFAULT_CONFIG["poll_interval"])
    doc["advanced"] = advanced
    
    with open(CONFIG_FILE, "w") as f:
        tomlkit.dump(doc, f)


def get_autostart_method():
    """Get current autostart method: 'xdg', 'systemd', or 'none'."""
    script = LIBDIR / "autostart.sh"
    if script.exists():
        result = subprocess.run([str(script), "--get"], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "none"
    return "none"


def set_autostart(method):
    """Set autostart method: 'xdg', 'systemd', or 'none'."""
    script = LIBDIR / "autostart.sh"
    if not script.exists():
        return
    
    if method == "xdg":
        subprocess.run([str(script), "--enable-xdg"], capture_output=True)
    elif method == "systemd":
        subprocess.run([str(script), "--enable-systemd"], capture_output=True)
    else:
        subprocess.run([str(script), "--disable"], capture_output=True)


def is_autostart_enabled():
    """Check if any autostart is enabled."""
    return get_autostart_method() != "none"