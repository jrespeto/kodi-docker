#!/bin/bash
set -e

# --- ENV defaults ---
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}
export DISPLAY=${DISPLAY:-:0}
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}
export PULSE_SERVER=${PULSE_SERVER:-unix:${XDG_RUNTIME_DIR}/pulse/native}

PROFILE=""
if [[ "$1" == "vpn" ]]; then
    # Check for OpenVPN config
    if [[ ! -f "ovpn-config/client.ovpn" ]]; then
        echo "❌ VPN mode requested but ovpn-config/client.ovpn not found."
        echo "   Please place your OpenVPN config at: ./ovpn-config/client.ovpn"
        exit 1
    fi

    PROFILE="--profile vpn"
    export KODI_NETWORK_MODE="service:openvpn-client"
else
    PROFILE="--profile kodi"
    export KODI_NETWORK_MODE="bridge"
fi

echo "🚀 Starting Kodi stack"
echo "  Mode: ${KODI_NETWORK_MODE}"
echo "  DISPLAY=${DISPLAY}"
echo "  WAYLAND_DISPLAY=${WAYLAND_DISPLAY}"
echo "  XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR}"
echo "  PULSE_SERVER=${PULSE_SERVER}"

# Allow local user access to XWayland (no-op on pure Wayland)
xhost +SI:localuser:$(whoami) >/dev/null 2>&1 || true

# Start containers
echo "running: podman-compose ${PROFILE} up -d"
podman-compose ${PROFILE} up -d
