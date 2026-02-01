<div align="center">
  <img src="res/icons/wgtray.svg" width="200px" alt="wgtray" />
  <h1>wgtray</h1>
  <p>A lightweight WireGuard system tray client for Linux.</p>
</div>

<p align="center">
  <a href="https://github.com/0xNatal/wgtray/releases">
    <img alt="GitHub Release" src="https://img.shields.io/github/v/release/0xNatal/wgtray" />
  </a>
  <a href="https://aur.archlinux.org/packages/wgtray">
    <img alt="AUR version" src="https://img.shields.io/aur/version/wgtray" />
  </a>
  <a href="https://github.com/0xNatal/wgtray/stargazers">
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/0xNatal/wgtray" />
  </a>
  <a href="https://github.com/0xNatal/wgtray/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/0xNatal/wgtray" />
  </a>
  <a href="https://www.gnu.org/licenses/gpl-3.0">
    <img alt="License: GPL v3" src="https://img.shields.io/badge/License-GPLv3-blue.svg" />
  </a>
</p>

> [!WARNING]
> **Work in Progress** – This project is under active development.

## Features

- Quick switch between VPN configurations
- Visual status indicator (connected/disconnected)
- Real-time status updates via Netlink
- Settings dialog with customization options
- Auto-connect on startup
- Uses standard `/etc/wireguard` configs
- Polkit integration for secure authentication
- Desktop notifications
- Left-click to toggle connection

## Roadmap

- [x] AUR package
- [x] Configuration file
- [x] Left-click quick action
- [x] About dialog
- [x] Real-time status updates (Netlink)
- [x] Settings dialog
- [x] Icon themes (light/dark)
- [x] Logging
- [ ] Keyboard shortcuts
- [ ] Support for other distributions (Ubuntu, Fedora, etc.)

## Requirements

- Arch Linux (or Arch-based)
- python-pyqt6
- python-pyroute2
- wireguard-tools
- polkit
- qt6-svg

## Installation

### AUR (recommended)

```bash
paru -S wgtray
# or: yay -S wgtray
```

### Manual

```bash
# Install dependencies
sudo pacman -S python-pyqt6 python-pyroute2 wireguard-tools polkit qt6-svg

# Clone and install
git clone https://github.com/0xNatal/wgtray.git
cd wgtray
sudo make install
```

## Usage

```bash
wgtray
```

The app starts minimized in the system tray.

- **Left-click**: Toggle last used connection
- **Right-click**: Open menu with all configurations

### Settings

Right-click → Settings to configure:

- Autostart on login
- Desktop notifications
- Auto-connect on startup
- Default VPN connection
- Icon theme
- Monitor mode (Netlink/Polling)
- Log level

Configuration is stored in `~/.config/wgtray/config.json`.

Logs are stored in `~/.local/share/wgtray/wgtray.log`.

### Troubleshooting

For debug output, run:

```bash
wgtray --debug
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

GPL-3.0 - see [LICENSE](LICENSE)