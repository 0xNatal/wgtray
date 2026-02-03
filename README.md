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
- CLI interface with autostart management
- Multiple autostart methods (XDG, Systemd)

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
- [x] CLI flags
- [x] Multiple autostart methods (XDG, Systemd)
- [ ] Auto-reconnect after suspend/resume
- [ ] Wait for network before auto-connect
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

> **Note:** Autostart is not enabled by default. See [Autostart](#autostart) to enable it.

- **Left-click**: Toggle last used connection
- **Right-click**: Open menu with all configurations

### CLI Options
```
wgtray [OPTIONS]

Options:
  -h, --help          Show help message
  -v, --version       Show version
  -d, --debug         Enable debug output
  --status            Show current autostart method
  --enable-xdg        Enable XDG autostart (Desktop Environments)
  --enable-systemd    Enable Systemd autostart (Window Managers)
  --disable           Disable autostart
```

### Autostart

To start wgtray automatically at boot, you can either:

**Desktop Environments** (KDE, GNOME, XFCE) – uses [XDG Autostart](https://wiki.archlinux.org/title/XDG_Autostart):
```bash
wgtray --enable-xdg
```

**Window Managers** (i3, Hyprland, Sway) – uses systemd user service:
```bash
wgtray --enable-systemd
```

**Manual** – add to your WM config:

Hyprland (`~/.config/hypr/hyprland.conf`):
```
exec-once = wgtray
```

i3 (`~/.config/i3/config`):
```
exec --no-startup-id wgtray
```

Sway (`~/.config/sway/config`):
```
exec wgtray
```

Check current method:
```bash
wgtray --status
```

Disable autostart:
```bash
wgtray --disable
```

### Settings

Right-click → Settings to configure:

- Autostart method (Off / XDG / Systemd)
- Desktop notifications
- Auto-connect on startup
- Require password
- Default VPN connection
- Icon theme
- Monitor mode (Netlink/Polling)
- Poll interval

Configuration is stored in `~/.config/wgtray/config.toml`.

Logs are stored in `~/.local/share/wgtray/wgtray.log`.

> [!NOTE]
> **Security:** When "Require password" is disabled, VPN connections can be started and stopped without authentication. Keep this enabled if you share your machine or run untrusted software.

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

**GNOME users:** GNOME does not support systray icons natively. Install the [AppIndicator extension](https://extensions.gnome.org/extension/615/appindicator-support/) for the tray icon to appear.

**Tray icon doesn't appear at startup:** This could be a [race condition](https://en.wikipedia.org/wiki/Race_condition#In_software). Add a delay:

- XDG: Edit `~/.config/autostart/wgtray.desktop`:
```
  Exec=/bin/sh -c "sleep 3 && wgtray"
```

- Systemd: Run `systemctl --user edit --full wgtray.service`:
```
  ExecStart=/bin/sh -c "sleep 3 && /usr/bin/wgtray"
```

Increase the `sleep` value if needed.

**Debug output:**
```bash
wgtray --debug
```

**Systemd logs:**
```bash
journalctl --user -u wgtray.service
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

GPL-3.0 - see [LICENSE](LICENSE)