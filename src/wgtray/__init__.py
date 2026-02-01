"""wgtray – a lightweight third-party WireGuard tray client"""

from .constants import VERSION

__version__ = VERSION
__all__ = ["WgTray"]

from .app import WgTray