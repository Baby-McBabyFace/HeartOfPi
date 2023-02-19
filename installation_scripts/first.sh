#!/bin/sh

echo "===================="
echo "Setting timezone..."
echo "===================="

sudo timedatectl set-timezone Asia/Singapore

echo "===================="
echo "Enabling VNC..."
echo "===================="

sudo systemctl enable vncserver-x11-serviced.service
sudo systemctl start vncserver-x11-serviced.service

echo "===================="
echo "Installing updates..."
echo "===================="

sudo apt update && sudo apt upgrade -y

echo "===================="
echo "Installing: Apache..."
echo "===================="

sudo apt install apache2 -y

echo "===================="
echo "Installing: Neofetch..."
echo "===================="

sudo apt install neofetch -y

sudo apt install figlet -y

sudo tee -a /home/pi/.bashrc <<EOF

figlet MDP-Team16
EOF

echo "===================="
echo "Installing: Python3-Pip..."
echo "===================="

sudo apt install python3-pip -y

echo "===================="
echo "Installing: Required libs..."
echo "===================="

sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran libopenblas-dev libopenmpi-dev libomp-dev -y


echo "===================="
echo "Installing: Python libs..."
echo "===================="

sudo apt install python3-picamera -y
pip3 install numpy
pip3 install Pillow
pip3 install opencv-python==4.5.3.56
pip3 install imagezmq
pip3 install imutils

echo "===================="
echo "Installing: Torch..."
echo "===================="

# sudo -H pip3 install setuptools==58.3.0
# sudo -H pip3 install Cython
# sudo -H pip3 install gdown
#
# gdown https://drive.google.com/uc?id=1E4bP9NAG5pDSXGWYPGsJ5uzFBq47VN14
# sudo -H pip3 install torch-1.8.0a0+37c1f4a-cp39-cp39-linux_aarch64.whl
# rm torch-1.8.0a0+37c1f4a-cp39-cp39-linux_aarch64.whl

echo "===================="
echo "Installing: samba..."
echo "===================="

sudo apt install samba samba-common-bin -y

echo "===================="
echo "Configuring Samba..."
echo "===================="

sudo tee -a /etc/samba/smb.conf <<EOF

[share]
path = /home/pi/
writeable = yes
browsable = yes
guest ok = yes
create mask = 0777
force user = pi
EOF

sudo systemctl enable smbd
sudo systemctl restart smbd

echo "===================="
echo "Installing: hostapd, dnsmasq..."
echo "===================="

sudo apt install hostapd dnsmasq -y

echo "===================="
echo "Installing: Netfilter, Iptables..."
echo "===================="

sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

echo "===================="
echo "Checking if Host Access Point configuration file exist..."
echo "===================="

if [ ! -f /etc/hostapd/hostapd.conf ]
then
echo "===================="
echo "Creating: Host Access Point configuration file..."
echo "===================="

sudo touch /etc/hostapd/hostapd.conf

echo "===================="
echo "Writing configuration..."
echo "===================="

sudo tee -a /etc/hostapd/hostapd.conf <<EOF
interface=wlan0
driver=nl80211
ssid=MDPGrp16
wpa_passphrase=2022Grp16
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
ieee80211n=1
wmm_enabled=1
EOF
else
    echo "===================="
    echo "Host Access Point configuration file exist. Skipping..."
    echo "===================="
fi

echo "===================="
echo "Replacing Host Access Point daemon file..."
echo "===================="

sudo sed -i 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/' /etc/default/hostapd

echo "===================="
echo "Creating: Pretty Hostname..."
echo "===================="

sudo touch /etc/machine-info

echo "===================="
echo "Changing Pretty Hostname..."
echo "===================="

sudo tee -a /etc/machine-info <<EOF
PRETTY_HOSTNAME=MDP-Team16
EOF

echo "===================="
echo "Changing Bluetooth mode to Compatible..."
echo "===================="

sudo sed -i 's/ExecStart=\/usr\/libexec\/bluetooth\/bluetoothd/ExecStart=\/usr\/libexec\/bluetooth\/bluetoothd -C --noplugin=sap \nExecStartPost=\/usr\/bin\/sdptool add SP/' /lib/systemd/system/bluetooth.service

echo "===================="
echo "Reload Bluetooth daemon..."
echo "===================="

sudo systemctl daemon-reload
sudo systemctl restart bluetooth

echo "===================="
echo "Setting to always enable bluetooth serial..."
echo "===================="

sudo sed -i 's/\nexit 0/\nsudo rfcomm watch hci0\n\nexit 0/' /etc/rc.local

echo "===================="
echo "Rebooting..."
echo "===================="

sleep 5
sudo reboot
