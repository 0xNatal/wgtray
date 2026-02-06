"""Hook system for wgtray."""

import subprocess
import os
from pathlib import Path
from .constants import HOOKS_DIR
from .logger import logger


def get_hook_path(interface: str, event: str) -> Path | None:
    """Get path to hook script if it exists."""
    hook = HOOKS_DIR / f"{interface}-{event}"
    if hook.exists() and hook.is_file():
        return hook
    return None


def run_hook(interface: str, event: str) -> tuple[bool, str | None]:
    """Run a hook script with sudo.
    
    Args:
        interface: WireGuard interface name (e.g., 'wg0')
        event: Hook event ('pre-connect', 'post-connect', 'pre-disconnect')
    
    Returns:
        Tuple of (success, error_message)
    """
    hook_path = get_hook_path(interface, event)
    if not hook_path:
        return True, None
    
    logger.info(f"Running hook: {hook_path}")
    
    try:
        result = subprocess.run(
            ["sudo", str(hook_path)],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "WGTRAY_INTERFACE": interface, "WGTRAY_EVENT": event}
        )
        
        if result.returncode != 0:
            error = result.stderr.strip() or f"Exit code {result.returncode}"
            logger.error(f"Hook failed: {hook_path}: {error}")
            return False, error
        
        if result.stdout.strip():
            logger.debug(f"Hook output: {result.stdout.strip()}")
        
        logger.info(f"Hook completed: {hook_path}")
        return True, None
        
    except subprocess.TimeoutExpired:
        logger.error(f"Hook timed out: {hook_path}")
        return False, "Timeout (30s)"
    except Exception as e:
        logger.error(f"Hook error: {hook_path}: {e}")
        return False, str(e)