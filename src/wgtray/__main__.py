#!/usr/bin/env python3
"""Entry point for wgtray."""

import sys
import signal
from .app import WgTray

# PySide6 blocks SIGINT by default
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    debug = "--debug" in sys.argv or "-d" in sys.argv
    app = WgTray(debug=debug)
    app.run()


if __name__ == "__main__":
    main()