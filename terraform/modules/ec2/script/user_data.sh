#!/bin/bash -xe

# Log everything
exec > >(tee /var/log/user-data.log) 2>&1

echo "Starting EC2 bootstrap at $(date)"

export DEBIAN_FRONTEND=noninteractive

# -----------------------------
# 1. SYSTEM UPDATE (SAFE ONLY)
# -----------------------------
apt-get update -y

# -----------------------------
# 2. CORE DEPENDENCIES
# -----------------------------
apt-get install -y \
  curl \
  ca-certificates \
  gnupg \
  lsb-release

# -----------------------------
# 3. DOCKER INSTALLATION
# -----------------------------
mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y

apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-compose-plugin

# Enable Docker
systemctl enable docker
systemctl start docker

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# -----------------------------
# 4. VERIFY INSTALLATION
# -----------------------------
docker --version
docker compose version

echo "Docker installation completed successfully"

# -----------------------------
# 5. OPTIONAL APP DIRECTORY
# -----------------------------
mkdir -p /home/ubuntu/app
chown ubuntu:ubuntu /home/ubuntu/app

echo "Bootstrap completed at $(date)"