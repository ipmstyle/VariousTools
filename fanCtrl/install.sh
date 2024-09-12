#!/bin/bash

# 파일 경로 설정
SRC_DIR=$(pwd)
DEST_BIN_DIR="/usr/local/bin"
SERVICE_FILE="/etc/systemd/system/fanctrl.service"

# 1. fanctrl.rb와 fanctrl_oneshot.rb를 /usr/local/bin으로 복사
echo "Copying fanctrl.rb and fanctrl_oneshot.rb to $DEST_BIN_DIR..."
sudo cp "$SRC_DIR/fanctrl.rb" "$DEST_BIN_DIR"
sudo cp "$SRC_DIR/fanctrl_oneshot.rb" "$DEST_BIN_DIR"

# 2. fanctrl.service를 /etc/systemd/system/으로 복사
echo "Copying fanctrl.service to /etc/systemd/system/..."
sudo cp "$SRC_DIR/fanctrl.service" "$SERVICE_FILE"

# 3. systemd 데몬 리로드
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# 4. fanctrl 서비스 활성화
echo "Enabling fanctrl.service..."
sudo systemctl enable fanctrl.service

# 5. fanctrl 서비스 시작
echo "Starting fanctrl.service..."
sudo systemctl start fanctrl.service

# 작업 완료
echo "Installation complete. fanctrl.service is now running."

