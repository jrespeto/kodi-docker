FROM ubuntu:noble
# FROM ubuntu:plucky

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    kodi* \
    locales \
    pulseaudio \
    tzdata \
    samba \
    smbclient \
    va-driver-all \
    intel-media-va-driver-non-free \
    i965-va-driver \
    mesa-va-drivers && \
    apt-get -y --purge autoremove && \
    rm -rf /var/lib/apt/lists/*

# setup entry point
COPY src/entrypoint.sh /usr/local/bin

RUN echo "America/New_York" > /etc/timezone
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
