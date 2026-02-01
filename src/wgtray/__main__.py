#!/usr/bin/env python3
"""Entry point for wgtray."""

import signal
from .app import WgTray

# PyQt blocks SIGINT by default
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    app = WgTray()
    app.run()


if __name__ == "__main__":
    main()