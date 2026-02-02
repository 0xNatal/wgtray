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
- Connection stats (traffic, last handshake)
- Real-time status updates via Netlink
- Hooks for pre-connect/post-connect/pre-disconnect scripts
- Settings dialog with customization options
- Auto-connect on startup
- Optional password authentication
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
- [x] Connection stats (traffic, handshake)
- [x] Hooks (pre-connect, post-connect, pre-disconnect)
- [x] Optional password requirement
- [ ] CLI flags
- [ ] Support for other distributions (Ubuntu, Fedora, etc.)

## Requirements

- Arch Linux (or Arch-based)
- pyside6
- python-pyroute2
- python-tomlkit
- wireguard-tools
- polkit

## Installation

### AUR (recommended)
```bash
paru -S wgtray
# or: yay -S wgtray
```

### Manual
```bash
# Install dependencies
sudo pacman -S pyside6 python-pyroute2 python-tomlkit wireguard-tools polkit

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
- Require password
- Default VPN connection
- Icon theme
- Monitor mode (Netlink/Polling)
- Poll interval

Configuration is stored in `~/.config/wgtray/config.toml`.

Logs are stored in `~/.local/share/wgtray/wgtray.log`.

### Hooks

Run custom scripts when connecting/disconnecting VPNs. Hooks run as your user (not root).

Create executable scripts in `~/.config/wgtray/hooks/`:
```bash
~/.config/wgtray/hooks/wg0.pre-connect      # Before connecting
~/.config/wgtray/hooks/wg0.post-connect     # After connecting
~/.config/wgtray/hooks/wg0.pre-disconnect   # Before disconnecting
```

**Hook naming:** `<interface>.<event>`

| Event | When |
|-------|------|
| `pre-connect` | Before connecting (after authentication) |
| `post-connect` | After successful connection |
| `pre-disconnect` | Before disconnecting (after authentication) |

**Environment variables available in hooks:**
- `WGTRAY_INTERFACE` – Interface name (e.g., `wg0`)
- `WGTRAY_EVENT` – Event type (`pre-connect`, `post-connect`, or `pre-disconnect`)

**Example hook:**
```bash
#!/bin/bash
# ~/.config/wgtray/hooks/wg0.post-connect
notify-send "Connected to $WGTRAY_INTERFACE"
```

Make executable: `chmod +x ~/.config/wgtray/hooks/wg0.post-connect`

### Troubleshooting

For debug output, run:
```bash
wgtray --debug
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

GPL-3.0 - see [LICENSE](LICENSE)