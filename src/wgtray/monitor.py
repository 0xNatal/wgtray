"""Network monitoring for wgtray."""

import time
from PySide6.QtCore import QThread, Signal
from .logger import logger


class NetlinkMonitor(QThread):
    """Monitor network interface changes via Netlink."""
    changed = Signal()

    def __init__(self):
        super().__init__()
        self._running = True
        self._available = False
        try:
            from pyroute2 import IPRoute
            with IPRoute():
                pass
            self._available = True
            logger.debug("Netlink monitoring available")
        except Exception as e:
            logger.warning(f"Netlink not available: {e}")

    @property
    def available(self):
        return self._available

    def run(self):
        if not self._available:
            return

        from pyroute2 import IPRoute
        with IPRoute() as ipr:
            ipr.bind()
            while self._running:
                try:
                    msgs = ipr.get(timeout=1)
                    for msg in msgs:
                        event = msg.get("event", "")
                        if event in ("RTM_NEWLINK", "RTM_DELLINK"):
                            attrs = dict(msg.get("attrs", []))
                            ifname = attrs.get("IFLA_IFNAME", "")
                            linkinfo = attrs.get("IFLA_LINKINFO")

                            is_wg = False
                            if linkinfo:
                                li_attrs = dict(linkinfo.get("attrs", []))
                                is_wg = li_attrs.get("IFLA_INFO_KIND") == "wireguard"

                            if is_wg or ifname.startswith("wg"):
                                logger.debug(f"Netlink: {ifname} {event}")
                                self.changed.emit()
                except Exception:
                    if self._running:
                        time.sleep(0.5)

    def stop(self):
        logger.debug("Stopping Netlink monitor")
        self._running = False
        self.wait(2000)