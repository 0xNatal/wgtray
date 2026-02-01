"""Configuration management for wgtray."""

import json
import shutil
from .constants import CONFIG_FILE, DEFAULT_CONFIG, AUTOSTART_FILE, SYSTEM_DESKTOP


def load_config():
    """Load config from file, merged with defaults."""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                user_config = json.load(f)
                config.update(user_config)
        except (json.JSONDecodeError, IOError):
            pass
    return config


def save_config(config):
    """Save config to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def is_autostart_enabled():
    """Check if autostart is enabled for current user."""
    return AUTOSTART_FILE.exists()


def set_autostart(enabled):
    """Enable or disable autostart."""
    AUTOSTART_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if enabled:
        if SYSTEM_DESKTOP.exists() and not AUTOSTART_FILE.exists():
            shutil.copy(SYSTEM_DESKTOP, AUTOSTART_FILE)
    else:
        if AUTOSTART_FILE.exists():
            AUTOSTART_FILE.unlink()