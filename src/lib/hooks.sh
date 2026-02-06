#!/bin/bash
set -euo pipefail

# Load constants
CONSTANTS="/usr/share/wgtray/constants.conf"
[[ -f "$CONSTANTS" ]] || CONSTANTS="$(dirname "$0")/../../res/constants.conf"
source "$CONSTANTS"

# Convert comma-separated to array
IFS=',' read -ra EVENTS_ARRAY <<< "$EVENTS"

validate_event() {
    local event="$1"
    for e in "${EVENTS_ARRAY[@]}"; do
        [[ "$event" == "$e" ]] && return 0
    done
    return 1
}

create_hook() {
    local iface="$1"
    local event="$2"
    local hook="$HOOKS_DIR/${iface}-${event}"
    local sudoers="$SUDOERS_DIR/wgtray-${iface}-${event}"
    
    if ! validate_event "$event"; then
        echo "Invalid event: $event" >&2
        echo "Valid events: $EVENTS" >&2
        exit 1
    fi
    
    # Create hooks directory
    sudo mkdir -p "$HOOKS_DIR"
    
    if [[ ! -f "$hook" ]]; then
        echo "Creating $hook..."
        sudo tee "$hook" > /dev/null << 'EOF'
#!/bin/bash
# wgtray hook script
# This runs as root. Add your privileged commands below.
#
# Available environment variables:
#   WGTRAY_INTERFACE - Interface name (e.g., wg0)
#   WGTRAY_EVENT     - Event type (pre-connect, post-connect, pre-disconnect)
#
# Examples:
#   mount /mnt/share
#   systemctl start my-service

EOF
        sudo chmod 755 "$hook"
        echo "✓ Created $hook"
    fi
    
    if [[ ! -f "$sudoers" ]]; then
        echo "Creating sudoers rule..."
        echo "$USER ALL=(ALL) NOPASSWD: $hook" | sudo tee "$sudoers" > /dev/null
        sudo chmod 440 "$sudoers"
        echo "✓ Created $sudoers"
    fi
    
    echo ""
    sudo "${EDITOR:-nano}" "$hook"
}

list_hooks() {
    if [[ ! -d "$HOOKS_DIR" ]]; then
        echo "No hooks found"
        return
    fi
    
    local found=false
    for hook in "$HOOKS_DIR"/*; do
        [[ -f "$hook" ]] || continue
        found=true
        basename "$hook"
    done
    $found || echo "No hooks found"
}

remove_hook() {
    local iface="$1"
    local event="$2"
    local hook="$HOOKS_DIR/${iface}-${event}"
    local sudoers="$SUDOERS_DIR/wgtray-${iface}-${event}"
    
    if [[ -f "$hook" ]]; then
        sudo rm "$hook"
        echo "✓ Removed $hook"
    else
        echo "Hook not found: $hook"
    fi
    
    if [[ -f "$sudoers" ]]; then
        sudo rm "$sudoers"
        echo "✓ Removed $sudoers"
    fi
}

case "${1:-}" in
    --create)
        [[ -z "${2:-}" || -z "${3:-}" ]] && { echo "Usage: hooks.sh --create <interface> <event>" >&2; exit 1; }
        create_hook "$2" "$3"
        ;;
    --list)
        list_hooks
        ;;
    --remove)
        [[ -z "${2:-}" || -z "${3:-}" ]] && { echo "Usage: hooks.sh --remove <interface> <event>" >&2; exit 1; }
        remove_hook "$2" "$3"
        ;;
    *)
        echo "Usage: hooks.sh [--create|--list|--remove] ..." >&2
        exit 1
        ;;
esac