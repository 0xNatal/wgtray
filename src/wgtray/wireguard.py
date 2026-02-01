"""WireGuard interface functions."""

import subprocess
import sys
import os
import time
from pathlib import Path
from .constants import LIBDIR
from .hooks import run_hook, ensure_hooks_dir
from .logger import logger


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


def connect(name):
    """Connect to a WireGuard VPN.
    
    Returns:
        Tuple of (success, hook_error) where hook_error is None or error message
    """
    ensure_hooks_dir()
    
    _, code = run_script("connect.sh", name, use_pkexec=True)
    
    if code == 0:
        hook_ok, hook_err = run_hook(name, "post-connect")
        if not hook_ok:
            logger.warning(f"Post-connect hook failed for {name}: {hook_err}")
        return True, hook_err if not hook_ok else None
    
    return False, None


def disconnect(name=None):
    """Disconnect from WireGuard VPN(s).
    
    Returns:
        Tuple of (success, hook_error) where hook_error is None or error message
    """
    ensure_hooks_dir()
    hook_errors = []
    
    if name:
        hook_ok, hook_err = run_hook(name, "pre-disconnect")
        if not hook_ok:
            hook_errors.append(f"{name}: {hook_err}")
        
        _, code = run_script("disconnect.sh", name, use_pkexec=True)
    else:
        active = get_active_connections()
        for iface in active:
            hook_ok, hook_err = run_hook(iface, "pre-disconnect")
            if not hook_ok:
                hook_errors.append(f"{iface}: {hook_err}")
        
        _, code = run_script("disconnect.sh", use_pkexec=True)
    
    hook_error = "; ".join(hook_errors) if hook_errors else None
    return code == 0, hook_error


def check_config_dir_permissions():
    """Ensure /etc/wireguard is readable."""
    config_dir = Path("/etc/wireguard")
    if config_dir.exists() and not os.access(config_dir, os.R_OK):
        subprocess.run(["pkexec", "chmod", "755", str(config_dir)], check=False)


def open_config_folder():
    """Open /etc/wireguard in file manager."""
    subprocess.run(["xdg-open", "/etc/wireguard"], check=False)