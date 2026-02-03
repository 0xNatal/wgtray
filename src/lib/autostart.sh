#!/bin/bash
set -euo pipefail

XDG_AUTOSTART_FILE="$HOME/.config/autostart/wgtray.desktop"
SYSTEM_DESKTOP="/usr/share/applications/wgtray.desktop"
SYSTEMD_SERVICE="wgtray.service"

get_method() {
    if systemctl --user is-enabled "$SYSTEMD_SERVICE" &>/dev/null; then
        echo "systemd"
    elif [[ -f "$XDG_AUTOSTART_FILE" ]]; then
        echo "xdg"
    else
        echo "none"
    fi
}

disable_all() {
    rm -f "$XDG_AUTOSTART_FILE"
    systemctl --user disable "$SYSTEMD_SERVICE" &>/dev/null || true
}

enable_xdg() {
    disable_all
    mkdir -p "$(dirname "$XDG_AUTOSTART_FILE")"
    cp "$SYSTEM_DESKTOP" "$XDG_AUTOSTART_FILE"
    echo "XDG autostart enabled"
}

enable_systemd() {
    disable_all
    systemctl --user enable "$SYSTEMD_SERVICE"
    echo "Systemd autostart enabled"
}

case "${1:-}" in
    --get)
        get_method
        ;;
    --enable-xdg)
        enable_xdg
        ;;
    --enable-systemd)
        enable_systemd
        ;;
    --disable)
        disable_all
        echo "Autostart disabled"
        ;;
    *)
        echo "Usage: autostart.sh [--get|--enable-xdg|--enable-systemd|--disable]" >&2
        exit 1
        ;;
esac