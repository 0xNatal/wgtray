#!/bin/bash
# Disconnect from WireGuard VPN
# Usage: disconnect.sh [config-name]
# Without argument: Disconnect all active connections

CONFIG_NAME="$1"

if [ -z "$CONFIG_NAME" ]; then
    ACTIVE=$(wg show interfaces 2>/dev/null)
    if [ -z "$ACTIVE" ]; then
        echo "No active connections"
        exit 0
    fi
    for iface in $ACTIVE; do
        wg-quick down "$iface" 2>&1
    done
    echo "All connections closed"
else
    if wg-quick down "$CONFIG_NAME" 2>&1; then
        echo "Disconnected from $CONFIG_NAME"
    else
        echo "Failed to disconnect from $CONFIG_NAME" >&2
        exit 1
    fi
fi