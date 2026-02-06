## [1.5.0] - 2026-02-06

### 🚀 Features

- [**breaking**] Run hooks as root with sudoers integration

### 📚 Documentation

- *(readme)* Add security note for require password setting

### ⚙️ Miscellaneous Tasks

- Add hooks migration warning to install script
- Clean up install output
## [1.4.0] - 2026-02-03

### 🚀 Features

- [**breaking**] Add CLI autostart management with XDG and systemd support

### 💼 Other

- V1.4.0

### 🚜 Refactor

- Switch config from JSON to TOML
- Switch from PyQt6 to PySide6
- Remove redundant disconnect button
- Replace print statements with logger

### 📚 Documentation

- Remove peer status from roadmap
- Update roadmap with D-Bus features
## [1.3.0] - 2026-02-01

### 🚀 Features

- Add logging with --debug flag
- Add logging and restructure settings dialog
- Show connection stats (traffic, handshake) in tooltip
- Add Python-based hook system
- Add hook system and optional password authentication

### 🐛 Bug Fixes

- Show correct logo

### 💼 Other

- V1.3.0

### 🚜 Refactor

- Move log path and refresh to settings dialog

### 📚 Documentation

- Update roadmap with new planned features
## [1.2.0] - 2026-02-01

### 🚀 Features

- Add light/dark icon theme support with auto-detection

### 🐛 Bug Fixes

- Stop running process before uninstall/upgrade
- Settings dialog icon path for new theme structure

### 💼 Other

- V1.2.0

### 📚 Documentation

- Update roadmap and releasing instructions
## [1.1.1] - 2026-02-01

### 🚀 Features

- Show ascii logo on installation

### 💼 Other

- V1.1.1
## [1.1.0] - 2026-02-01

### 🚀 Features

- Add left-click toggle and config file for last connection
- Add about dialog
- [**breaking**] Restructure as package, add settings and netlink monitoring

### 💼 Other

- V1.1.0

### 📚 Documentation

- Add AUR badge
- Remove connection timer (not useful with 30s refresh)
- Add settings documentation to readme

### 🎨 Styling

- Remove dot from tray icon
- Improve menu layout with checkmark for active connection

### ⚙️ Miscellaneous Tasks

- Update release script for new package structure
## [1.0.2] - 2026-01-31

### 🚀 Features

- Add post-upgrade message

### 💼 Other

- V1.0.2
## [1.0.1] - 2026-01-31

### 🚀 Features

- Add GNOME autostart flag

### 💼 Other

- V1.0.1

### 📚 Documentation

- Mark AUR package as complete
- Improve post-install message
## [1.0.0] - 2026-01-31

### 🚀 Features

- Add main application and helper scripts
- Add icons, desktop file and polkit policy

### 💼 Other

- Add Makefile and PKGBUILD for AUR
- V1.0.0

### 🚜 Refactor

- Improve permission handling for config directory

### 📚 Documentation

- Add initial README with WIP notice
- Restructure README with centered layout
- Add badges for release, stars, issues and AUR votes
- Fix GitHub username in badge URLs
- Increase logo size
- Add security policy
- Update README with features, roadmap and installation

### ⚙️ Miscellaneous Tasks

- Initial project setup
- Remove unused icons
