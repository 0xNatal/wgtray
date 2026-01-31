PKGNAME = wgtray
PREFIX ?= /usr

ICONS = $(wildcard res/icons/*.svg)

.PHONY: all check-deps install uninstall

all:
	@echo "Usage:"
	@echo "  sudo make install"
	@echo "  sudo make uninstall"
	@echo "  make check-deps"

check-deps:
	@echo "Checking dependencies..."
	@command -v python3 >/dev/null || { echo "ERROR: python3 not found"; exit 1; }
	@python3 -c "from PyQt6.QtWidgets import QApplication" 2>/dev/null || { echo "ERROR: PyQt6 not found. Install: sudo pacman -S python-pyqt6"; exit 1; }
	@command -v wg >/dev/null || { echo "ERROR: wireguard-tools not found. Install: sudo pacman -S wireguard-tools"; exit 1; }
	@command -v pkexec >/dev/null || { echo "ERROR: polkit not found. Install: sudo pacman -S polkit"; exit 1; }
	@echo "All dependencies found!"

install:
	install -Dm755 src/wgtray.py $(DESTDIR)$(PREFIX)/bin/$(PKGNAME)
	install -Dm755 -t $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/lib src/lib/*.sh
	install -Dm644 -t $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps $(ICONS)
	install -Dm644 res/desktop/$(PKGNAME).desktop $(DESTDIR)$(PREFIX)/share/applications/$(PKGNAME).desktop
	install -Dm644 res/desktop/$(PKGNAME).desktop $(DESTDIR)/etc/xdg/autostart/$(PKGNAME).desktop
	install -Dm644 res/polkit/org.$(PKGNAME).policy $(DESTDIR)$(PREFIX)/share/polkit-1/actions/org.$(PKGNAME).policy
	install -Dm644 README.md $(DESTDIR)$(PREFIX)/share/doc/$(PKGNAME)/README.md
	install -Dm644 LICENSE $(DESTDIR)$(PREFIX)/share/doc/$(PKGNAME)/LICENSE
	@echo ""
	@echo "Installation complete!"
	@echo "Run 'wgtray' to start, or logout/login for autostart."

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/$(PKGNAME)
	rm -rf $(DESTDIR)$(PREFIX)/share/$(PKGNAME)
	rm -f $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps/wgtray*.svg
	rm -f $(DESTDIR)$(PREFIX)/share/applications/$(PKGNAME).desktop
	rm -f $(DESTDIR)/etc/xdg/autostart/$(PKGNAME).desktop
	rm -f $(DESTDIR)$(PREFIX)/share/polkit-1/actions/org.$(PKGNAME).policy
	rm -rf $(DESTDIR)$(PREFIX)/share/doc/$(PKGNAME)
	@echo "Uninstall complete!"