#!/bin/bash
# List available WireGuard configurations

CONFIG_DIR="${WG_TRAY_CONFIG_DIR:-/etc/wireguard}"

if [ -d "$CONFIG_DIR" ]; then
    for conf in "$CONFIG_DIR"/*.conf; do
        [ -f "$conf" ] || continue
        basename "$conf" .conf
    done | sort
fi
