#!/usr/bin/env bash
set -e                                # exit on error immediately
USER_NAME=$(logname 2>/dev/null)      # Log the username who ran sudo

# OpenSearchAPI Setup Script - SudoHopeX


# verify script is executed with sudo permissions
if [ "$EUID" -ne 0 ]; then
  echo "[!] This script must be run with sudo."
  exit 1
fi

# update system
echo "[+] Updating the System..."
if apt update > /dev/null 2>&1; then
  echo "[✓] System Updated..."
else
  echo "[!] System Update failed."
  exit 1
fi


# installing dependencies if not found on system
install_if_missing() {
    for pkg in "$@"; do
      if ! dpkg -s "$pkg" >/dev/null 2>&1; then
          echo "$pkg Installing..."
          apt-get install "$pkg" -y > /dev/null 2>&1
          echo "$pkg Installation Complete"
      else
          echo "[✓] $pkg is already installed."
      fi
    done
}

# install system packages
echo ""
echo "[+] System Requirements Check..."
install_if_missing chromium python3 python3-pip python3-venv xvfb


# make folder within /opt dir
mkdir -p /opt/OpenSearchAPI
cd /opt/OpenSearchAPI


# clone the github repo
echo ""
echo "Cloning GitHub Repo 'OpenSearchAPI'"
git clone https://github.com/SudoHopeX/OpenSearchAPI.git /opt/OpenSearchAPI > /dev/null 2>&1

# make python venv
python -m venv /opt/OpenSearchAPI/its_venv
source /opt/OpenSearchAPI/its_venv/bin/activate

# install pip requirements
echo "[+] Installing pip Requirements..."
pip install requests beautifulsoup4 flask ddgs curl_cffi nodriver pyvirtualdisplay > /dev/null 2>&1


# create a simple launcher for starting OpenSearchAPI in bg
sudo tee /usr/local/bin/opensearchapi > /dev/null <<'EOF'
#!/usr/bin/env bash

echo "SudoHopeX - OpenSearchAPI"

source /opt/OpenSearchAPI/its_venv/bin/activate
python /opt/OpenSearchAPI/app.py

deactivate
EOF


chmod +x /usr/local/bin/opensearchapi

# changing the ownership of /opt/OpenSearchAPI to the actual user who ran sudo
chown -R "$USER_NAME":"$USER_NAME" /opt/OpenSearchAPI/

# test the launcher
opensearchapi