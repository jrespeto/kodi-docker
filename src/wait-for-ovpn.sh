#!/bin/sh

openvpn --config /etc/openvpn/client.conf &

danted -f /etc/sockd.conf
