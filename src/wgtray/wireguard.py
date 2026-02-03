"""WireGuard interface functions."""

import subprocess
import sys
import os
import time
from pathlib import Path
from .constants import LIBDIR, HOOKS_DIR
from .hooks import run_hook
from .logger import logger


def run_script(script_name, *args, use_pkexec=False):
    """Run a helper script, optionally with pkexec for root privileges."""
    script_path = LIBDIR / script_name
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
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


def authenticate() -> bool:
    """Trigger pkexec authentication.
    
    Returns:
        True if authentication succeeded, False if cancelled/failed.
    """
    auth_script = LIBDIR / "auth.sh"
    if not auth_script.exists():
        logger.warning(f"Auth script not found: {auth_script}")
        return True
    
    try:
        result = subprocess.run(
            ["pkexec", str(auth_script)],
            capture_output=True,
            timeout=60
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.error("Authentication timed out")
        return False
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return False


def ensure_hooks_dir():
    """Create hooks directory if it doesn't exist."""
    HOOKS_DIR.mkdir(parents=True, exist_ok=True)


def get_active_connections():
    """Get list of active WireGuard interfaces."""
    output, code = run_script("status.sh")
    if code == 0 and output:
        return [x for x in output.split("\n") if x]
    return []


def get_configs():
    """Get list of available WireGuard configurations."""
    output, code = run_script("list-configs.sh")
    if code == 0 and output:
        return [x for x in output.split("\n") if x]
    return []


def get_connection_stats(interface):
    """Get connection stats for a WireGuard interface."""
    output, code = run_script("stats.sh", interface, use_pkexec=True)
    if code != 0 or not output:
        return None
    
    try:
        parts = output.split()
        if len(parts) >= 3:
            return {
                "rx_bytes": int(parts[0]),
                "tx_bytes": int(parts[1]),
                "latest_handshake": int(parts[2]) if int(parts[2]) > 0 else None
            }
    except (ValueError, IndexError):
        pass
    return None


def format_bytes(bytes_val):
    """Format bytes to human readable string."""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"


def format_handshake(timestamp):
    """Format handshake timestamp to human readable string."""
    if not timestamp:
        return "never"
    
    diff = int(time.time()) - timestamp
    
    if diff < 60:
        return f"{diff}s ago"
    elif diff < 3600:
        return f"{diff // 60}m ago"
    elif diff < 86400:
        return f"{diff // 3600}h ago"
    else:
        return f"{diff // 86400}d ago"


def connect(name, require_password=True):
    """Connect to a WireGuard VPN.
    
    Returns:
        Tuple of (success, hook_error, cancelled)
    """
    ensure_hooks_dir()
    
    # Authenticate if required
    if require_password:
        if not authenticate():
            logger.info("Authentication cancelled")
            return False, None, True
    
    # Pre-connect hook
    hook_ok, hook_err = run_hook(name, "pre-connect")
    if not hook_ok:
        logger.warning(f"Pre-connect hook failed for {name}: {hook_err}")
    
    # Connect
    _, code = run_script("connect.sh", name, use_pkexec=True)
    
    if code == 0:
        # Post-connect hook
        hook_ok, hook_err = run_hook(name, "post-connect")
        if not hook_ok:
            logger.warning(f"Post-connect hook failed for {name}: {hook_err}")
        return True, hook_err if not hook_ok else None, False
    
    return False, None, False


def disconnect(name=None, require_password=True):
    """Disconnect from WireGuard VPN(s).
    
    Returns:
        Tuple of (success, hook_error, cancelled)
    """
    ensure_hooks_dir()
    hook_errors = []
    
    # Get interfaces
    interfaces = [name] if name else get_active_connections()
    if not interfaces:
        return True, None, False
    
    # Authenticate if required
    if require_password:
        if not authenticate():
            logger.info("Authentication cancelled")
            return False, None, True
    
    # Pre-disconnect hooks
    for iface in interfaces:
        hook_ok, hook_err = run_hook(iface, "pre-disconnect")
        if not hook_ok:
            hook_errors.append(f"{iface}: {hook_err}")
    
    # Disconnect
    if name:
        _, code = run_script("disconnect.sh", name, use_pkexec=True)
    else:
        _, code = run_script("disconnect.sh", use_pkexec=True)
    
    hook_error = "; ".join(hook_errors) if hook_errors else None
    return code == 0, hook_error, False


def check_config_dir_permissions():
    """Ensure /etc/wireguard is readable."""
    config_dir = Path("/etc/wireguard")
    if config_dir.exists() and not os.access(config_dir, os.R_OK):
        subprocess.run(["pkexec", "chmod", "755", str(config_dir)], check=False)


def open_config_folder():
    """Open /etc/wireguard in file manager."""
    subprocess.run(["xdg-open", "/etc/wireguard"], check=False)