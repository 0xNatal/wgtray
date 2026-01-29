# wgtray

<p align="center">
  <img width="200" height="200" src="res/icons/wgtray.svg">
</p>

[![AUR version](https://img.shields.io/aur/version/wgtray)](https://aur.archlinux.org/packages/wgtray)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A simple WireGuard system tray client for Linux.

## Features

- 🔄 Quick switch between VPN configurations
- 🟢 Visual status indicator (connected/disconnected)
- 📁 Uses standard `/etc/wireguard` configs
- 🔐 Polkit integration for secure authentication
- 🖱️ Simple right-click menu
- 🔔 Desktop notifications
- ⏱️ Auto-refresh status every 30 seconds

## Installation

### From AUR (Arch Linux / CachyOS)

```bash
yay -S wgtray
```

### From Source

Install required dependencies:

```bash
sudo pacman -S --needed python-pyqt6 wireguard-tools polkit qt6-svg
```

Download and install:

```bash
git clone https://github.com/DEIN_USER/wgtray.git
cd wgtray
sudo make install
```

To uninstall:

```bash
sudo make uninstall
```

## Usage

### Starting the tray applet

Launch from your application menu or run:

```bash
wgtray
```

### Autostart

The application automatically starts at login after installation. To disable autostart:

```bash
rm ~/.config/autostart/wgtray.desktop
```

To manually enable autostart:

```bash
# If installed from AUR:
cp /usr/share/applications/wgtray.desktop ~/.config/autostart/

# If installed with make install:
cp /usr/local/share/applications/wgtray.desktop ~/.config/autostart/
```

## Configuration

### WireGuard configs

Place your WireGuard configuration files in `/etc/wireguard/`:

```bash
sudo cp my-vpn.conf /etc/wireguard/
sudo chmod 600 /etc/wireguard/my-vpn.conf
```

### Custom config directory

To use a different directory:

```bash
export WG_TRAY_CONFIG_DIR=~/.config/wireguard
wgtray
```

## Dependencies

- `python-pyqt6` - GUI framework
- `wireguard-tools` - WireGuard utilities (wg, wg-quick)
- `polkit` - Authentication for root access
- `qt6-svg` - SVG icon support

## Troubleshooting

### No tray icon visible (GNOME)

Install the AppIndicator extension:

```bash
sudo pacman -S gnome-shell-extension-appindicator
```

Then enable it in GNOME Extensions.

### Authentication fails

Make sure polkit is running:

```bash
systemctl status polkit
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.