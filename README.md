# Kodi + OpenVPN (Podman Compose)

This project provides a containerized **Kodi media center** environment with optional **OpenVPN client support**.
It is designed for **testing Kodi plugins** in a reproducible, isolated environment with modern **Wayland + PipeWire/PulseAudio** support.

---

## 📦 Features

- Run **Kodi inside a container** with GPU acceleration (Intel iGPU or NVIDIA GPU).
- Optional **OpenVPN client container** for secure traffic routing.
- Toggle VPN mode easily with `./start.sh vpn` (no manual edits required).
- Wayland & XWayland support (for GUI display).
- PipeWire/PulseAudio passthrough for audio.
- Persistent Kodi configuration via `./kodi_home/.kodi`.
- Ideal for **Kodi plugin development & testing**.

---

## 🔧 Prerequisites

- Linux host with:
  - [Podman](https://podman.io/) + [podman-compose](https://github.com/containers/podman-compose)
  - A **Wayland desktop session** (XWayland installed for fallback)
  - PulseAudio or PipeWire (with PulseAudio emulation)
  - GPU drivers installed:
    - Intel: `va-driver-all`, `intel-media-va-driver-non-free`
    - NVIDIA: proprietary drivers + `nvidia-container-toolkit`
- An OpenVPN `.ovpn` config file (optional, for VPN testing)

---

## 📂 File structure

```

.
├── Docker/
│   ├── Dockerfile        # Kodi image
│   ├── Dockerfile-ovpn   # OpenVPN client image
├── kodi\_home/            # Persistent Kodi config
├── ovpn-config/
│   └── client.ovpn       # Your VPN config
├── src/
│   ├── entrypoint.sh     # Kodi startup script
│   ├── wait-for-ovpn.sh  # OVPN startup wrapper
│   └── sockd.conf        # (optional) SOCKS5 proxy config
├── docker-compose.yml
├── start.sh              # Launcher script
└── README.md

````

---

## ⚙️ Configuration

### Environment setup (handled by `start.sh`)

`start.sh` automatically configures:

- `DISPLAY` → your X11/XWayland display (defaults to `:0`)
- `WAYLAND_DISPLAY` → defaults to `wayland-0`
- `XDG_RUNTIME_DIR` → defaults to `/run/user/$(id -u)`
- `PULSE_SERVER` → defaults to `unix:${XDG_RUNTIME_DIR}/pulse/native`

No manual `.env` file is required.

---

## ▶️ Usage

### Start Kodi (no VPN)
```bash
./start.sh
````

* Starts Kodi container only
* Sets `network_mode=bridge`
* Suitable for local plugin development/testing

---

### Start Kodi (with VPN)

```bash
./start.sh vpn
```

* Starts both `openvpn-client` and Kodi
* Sets `KODI_NETWORK_MODE=service:openvpn-client`
* Kodi routes all traffic through VPN container

---

### Logs

* Kodi logs:

  ```bash
  podman logs -f kodi
  ```
* OpenVPN logs:

  ```bash
  podman logs -f openvpn-client
  ```

---

## 🧪 Testing Kodi Plugins

### 1. Mount your plugin

Place your plugin under `./kodi_home/.kodi/addons/`.
For hot-reload development, you can mount your source folder in `docker-compose.yml`:

```yaml
volumes:
  - ./my-plugin:/root/.kodi/addons/my-plugin:rw
```

### 2. Enable debugging

Inside Kodi:

* Go to: **Settings → System → Logging → Enable debug logging**
* Test your add-on
* Logs available at:

  ```bash
  ./kodi_home/.kodi/temp/kodi.log
  ```

### 3. VPN testing

Run with `./start.sh vpn` to test:

* Region-locked streams
* VPN-specific behavior
* Geo-blocked APIs

---

## 🔍 Verifying VPN Routing

To check if Kodi traffic goes through VPN:

```bash
podman exec -it kodi curl ifconfig.me
```

* Without VPN → shows your ISP/public IP
* With VPN → shows VPN provider’s IP

---

## 🛠️ Troubleshooting

* **Kodi GUI won’t start**
  Ensure you have XWayland installed. Test with:

  ```bash
  echo $DISPLAY
  ```

  If unset, add `export DISPLAY=:0` in your shell before running `./start.sh`.

* **No sound**
  Check PipeWire/PulseAudio server:

  ```bash
  pactl info | grep "Server String"
  ```

  Ensure it matches what `PULSE_SERVER` is set to in logs.

* **VPN won’t connect**
  Verify your `.ovpn` config at `./ovpn-config/client.ovpn`.

* **Debug logs**
  Check `./kodi_home/.kodi/temp/kodi.log` or container logs with `podman logs`.

---

## 📚 References

* [Kodi Official Wiki](https://kodi.wiki/)
* [OpenVPN Docs](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/)
* [Podman Compose](https://github.com/containers/podman-compose)
* [PipeWire](https://pipewire.org/)

---

## ✅ Summary

* Run `./start.sh` → Kodi in bridge mode (no VPN)
* Run `./start.sh vpn` → Kodi routed through OpenVPN container
* Wayland + PipeWire ready
* Perfect for **plugin testing** with or without VPN

