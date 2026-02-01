"""Hook system for wgtray."""

import subprocess
import os
from pathlib import Path
from .constants import HOOKS_DIR
from .logger import logger


def get_hook_path(interface: str, event: str) -> Path | None:
    """Get path to hook script if it exists and is executable."""
    hook = HOOKS_DIR / f"{interface}.{event}"
    if hook.exists() and hook.is_file():
        if not hook.stat().st_mode & 0o100:
            logger.warning(f"Hook exists but not executable: {hook}")
            return None
        return hook
    return None


def run_hook(interface: str, event: str) -> tuple[bool, str | None]:
    """Run a hook script.
    
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
            [str(hook_path)],
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
    except PermissionError:
        logger.error(f"Hook permission denied: {hook_path}")
        return False, "Permission denied"
    except Exception as e:
        logger.error(f"Hook error: {hook_path}: {e}")
        return False, str(e)


def ensure_hooks_dir():
    """Create hooks directory if it doesn't exist."""
    HOOKS_DIR.mkdir(parents=True, exist_ok=True)