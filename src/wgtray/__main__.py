#!/usr/bin/env python3
"""Entry point for wgtray."""

import sys
import signal
import fcntl
from pathlib import Path

from .app import WgTray

LOCK_FILE = Path.home() / ".cache" / "wgtray.lock"


def acquire_lock():
    """Acquire single-instance lock. Returns lock file handle or None."""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    lock_fd = open(LOCK_FILE, 'w')
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except BlockingIOError:
        lock_fd.close()
        return None


def main():
    debug = "--debug" in sys.argv or "-d" in sys.argv
    
    lock = acquire_lock()
    if lock is None:
        print("wgtray is already running", file=sys.stderr)
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = WgTray(debug=debug)
    app.run()


if __name__ == "__main__":
    main()