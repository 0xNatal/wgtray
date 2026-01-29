#!/bin/bash
# Connect to a WireGuard VPN
# Usage: connect.sh <config-name>

CONFIG_NAME="$1"

if [ -z "$CONFIG_NAME" ]; then
    echo "Error: No config name provided" >&2
    exit 1
fi

if wg-quick up "$CONFIG_NAME" 2>&1; then
    echo "Connected to $CONFIG_NAME"
else
    echo "Failed to connect to $CONFIG_NAME" >&2
    exit 1
fi