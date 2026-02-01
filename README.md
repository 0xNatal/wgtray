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
- Uses standard `/etc/wireguard` configs
- Polkit integration for secure authentication
- Desktop notifications
- Auto-refresh status

## Roadmap

- [x] AUR package
- [ ] Settings dialog
- [x] Configuration file
- [x] Left-click quick action
- [ ] About dialog
- [ ] Keyboard shortcuts
- [ ] Real-time status updates (filesystem watching)
- [ ] Logging
- [ ] Icon themes (light/dark)
- [ ] Support for other distributions (Ubuntu, Fedora, etc.)

## Requirements

- Arch Linux (or Arch-based)
- python-pyqt6
- wireguard-tools
- polkit

## Installation

```bash
git clone https://github.com/0xNatal/wgtray.git
cd wgtray
sudo make install
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

GPL-3.0 - see [LICENSE](LICENSE)