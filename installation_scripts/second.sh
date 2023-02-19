#!/bin/sh

echo "===================="
echo "Unmasking and starting Host Access Point daemon..."
echo "===================="

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

echo "===================="
echo "Host Access Point daemon Status"
echo "===================="

sudo systemctl status hostapd --no-pager

echo "===================="
echo "Configuring Wireless interface wlan0"
echo "===================="

sudo tee -a /etc/dhcpcd.conf <<EOF
interface wlan0
static ip_address=192.168.16.16/24
nohook wpa_supplicant
EOF

echo "===================="
echo "Configuring DHCP Server"
echo "===================="

sudo tee -a /etc/dnsmasq.conf <<EOF
interface=wlan0
dhcp-range=192.168.16.20,192.168.16.60,255.255.255.0,24h
EOF

echo "===================="
echo "Restarting DHCP Server"
echo "===================="

sudo systemctl restart dnsmasq

echo "===================="
echo "DHCP daemon Status"
echo "===================="

sudo systemctl status dnsmasq --no-pager

echo "===================="
echo "Enable packet forwarding"
echo "===================="

sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

echo "===================="
echo "Adding iptable rules"
echo "===================="

sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED, ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

echo "===================="
echo "Verifying iptable rules"
echo "===================="

sudo iptables -t nat -S
sudo iptables -S

echo "===================="
echo "Saving iptable rules"
echo "===================="

sudo iptables-save | sudo tee /etc/iptables.ipv4.nat

sudo netfilter-persistent save

echo "===================="
echo "Rebooting..."
echo "===================="

sleep 5
sudo reboot