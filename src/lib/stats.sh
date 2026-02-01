#!/bin/bash
# Get WireGuard connection stats
# Usage: stats.sh <interface>
# Output: rx_bytes tx_bytes latest_handshake

INTERFACE="$1"

if [ -z "$INTERFACE" ]; then
    echo "Error: No interface provided" >&2
    exit 1
fi

# Get dump output (needs root, but wg show works without for basic info)
DUMP=$(wg show "$INTERFACE" dump 2>/dev/null)

if [ -z "$DUMP" ]; then
    exit 1
fi

# Skip first line (interface), sum up peer stats
RX_TOTAL=0
TX_TOTAL=0
LATEST_HS=0

while IFS=$'\t' read -r pubkey psk endpoint allowed_ips handshake rx tx keepalive; do
    # Skip interface line (has different format)
    [ -z "$rx" ] && continue
    
    RX_TOTAL=$((RX_TOTAL + rx))
    TX_TOTAL=$((TX_TOTAL + tx))
    
    if [ "$handshake" -gt "$LATEST_HS" ] 2>/dev/null; then
        LATEST_HS="$handshake"
    fi
done <<< "$DUMP"

echo "$RX_TOTAL $TX_TOTAL $LATEST_HS"