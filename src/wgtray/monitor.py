"""Network monitoring for wgtray."""

import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal


class NetlinkMonitor(QThread):
    """Monitor network interface changes via Netlink."""
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._running = True
        self._available = False
        try:
            from pyroute2 import IPRoute
            with IPRoute():
                pass
            self._available = True
        except Exception as e:
            print(f"Netlink not available: {e}", file=sys.stderr)

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
                                self.changed.emit()
                except Exception:
                    if self._running:
                        time.sleep(0.5)

    def stop(self):
        self._running = False
        self.wait(2000)