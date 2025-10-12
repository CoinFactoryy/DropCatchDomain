# Quick Start: Deploy to Linode

## 🚀 One-Command Deployment

```bash
# 1. Create Linode instance (Ubuntu 22.04, Nanode 1GB)
# 2. Connect via SSH
ssh root@YOUR_LINODE_IP

# 3. Clone your repository
git clone https://github.com/YOUR_USERNAME/DropCatchDomain.git
cd DropCatchDomain

# 4. Run deployment script
sudo ./deploy-linode.sh

# 5. Configure environment variables
nano .env  # Add your API keys

# 6. Restart service
sudo systemctl restart domain-catcher
```

## ⚡ What the Script Does

- ✅ Updates system packages
- ✅ Installs Python, nginx, git, ufw
- ✅ Creates `domaincatcher` user
- ✅ Sets up virtual environment
- ✅ Installs Python dependencies
- ✅ Creates systemd service
- ✅ Configures nginx reverse proxy
- ✅ Sets up firewall rules
- ✅ Starts all services

## 🔧 Manual Steps After Deployment

1. **Edit API Keys**: `nano .env`
2. **Restart Service**: `sudo systemctl restart domain-catcher`
3. **Check Status**: `sudo systemctl status domain-catcher`
4. **View Logs**: `sudo journalctl -u domain-catcher -f`

## 🌐 Access Your Application

- **Health Check**: `http://YOUR_LINODE_IP/health`
- **Application**: `http://YOUR_LINODE_IP/`

## 📊 Management Commands

```bash
# Service management
sudo systemctl status domain-catcher
sudo systemctl restart domain-catcher
sudo systemctl stop domain-catcher
sudo systemctl start domain-catcher

# View logs
sudo journalctl -u domain-catcher -f
tail -f /home/domaincatcher/DropCatchDomain/domain_catcher.log

# Update application
sudo su - domaincatcher
cd DropCatchDomain
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart domain-catcher
```

## 🔒 Security Setup (Optional)

```bash
# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d YOUR_DOMAIN

# Setup automatic updates
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

## 💰 Cost: ~$5/month

Your domain monitoring system will run 24/7 with full control and access!
