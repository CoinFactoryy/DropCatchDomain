# Linode Deployment Guide for Domain Catcher

This guide will help you deploy your Python domain monitoring script on a Linode VPS with full control and access.

## 🚀 Quick Setup

### 1. Create Linode Instance

1. **Sign up**: Go to [linode.com](https://linode.com) and create an account
2. **Create Instance**: 
   - Choose Ubuntu 22.04 LTS
   - Select Nanode 1GB plan ($5/month) - sufficient for this application
   - Choose a datacenter close to you
   - Set root password and SSH key
3. **Boot Instance**: Click "Create Linode"

### 2. Initial Server Setup

```bash
# Connect to your Linode
ssh root@YOUR_LINODE_IP

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3 python3-pip python3-venv nginx git -y

# Create application user
adduser --disabled-password --gecos "" domaincatcher
usermod -aG sudo domaincatcher
```

### 3. Deploy Application

```bash
# Switch to application user
su - domaincatcher

# Clone your repository
git clone https://github.com/YOUR_USERNAME/DropCatchDomain.git
cd DropCatchDomain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
nano .env  # Edit with your API keys
```

### 4. Configure Environment Variables

Edit `.env` file with your API keys:

```env
DYNADOT_API_KEY=your_dynadot_api_key
PORKBUN_API_KEY=your_porkbun_api_key
PORKBUN_SECRET_KEY=your_porkbun_secret_key
DISCORD_WEBHOOK=your_discord_webhook_url
LOG_LEVEL=INFO
```

### 5. Setup Systemd Service

The systemd service file will be created automatically by the deployment script.

### 6. Configure Nginx

The nginx configuration will be set up to proxy requests to your Flask application.

### 7. Start Services

```bash
# Enable and start the service
sudo systemctl enable domain-catcher
sudo systemctl start domain-catcher

# Check status
sudo systemctl status domain-catcher

# Enable nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

## 🔧 Manual Configuration

### Systemd Service File

Create `/etc/systemd/system/domain-catcher.service`:

```ini
[Unit]
Description=Domain Catcher Service
After=network.target

[Service]
Type=simple
User=domaincatcher
Group=domaincatcher
WorkingDirectory=/home/domaincatcher/DropCatchDomain
Environment=PATH=/home/domaincatcher/DropCatchDomain/venv/bin
ExecStart=/home/domaincatcher/DropCatchDomain/venv/bin/python health_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration

Create `/etc/nginx/sites-available/domain-catcher`:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/domain-catcher /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 📊 Monitoring & Management

### Check Service Status
```bash
sudo systemctl status domain-catcher
sudo journalctl -u domain-catcher -f
```

### View Logs
```bash
tail -f /home/domaincatcher/DropCatchDomain/domain_catcher.log
```

### Restart Service
```bash
sudo systemctl restart domain-catcher
```

### Update Application
```bash
su - domaincatcher
cd DropCatchDomain
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart domain-catcher
```

## 🔒 Security Considerations

### Firewall Setup
```bash
# Install ufw
sudo apt install ufw -y

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### SSL Certificate (Optional)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d YOUR_DOMAIN
```

## 💰 Cost Breakdown

- **Linode Nanode**: $5/month (1GB RAM, 1 CPU, 25GB SSD)
- **Domain**: ~$10-15/year (optional)
- **Total**: ~$5-6/month

## 🆚 Linode vs Render Comparison

| Feature | Linode | Render |
|---------|--------|--------|
| **Cost** | $5/month | Free (750 hours) |
| **Control** | Full root access | Limited |
| **Uptime** | 99.9% SLA | No SLA |
| **Customization** | Complete | Limited |
| **File System** | Full access | Ephemeral |
| **Background Tasks** | Supported | Limited |
| **Database** | Any type | Limited options |
| **SSL** | Free with Let's Encrypt | Included |
| **Monitoring** | Full system access | Application only |

## 🚀 Advantages of Linode Deployment

1. **Full Control**: Root access to the entire system
2. **Persistent Storage**: Files persist between deployments
3. **Custom Configuration**: Install any software you need
4. **Better Performance**: Dedicated resources
5. **Reliability**: 99.9% uptime SLA
6. **Cost Effective**: Predictable monthly pricing
7. **Scalability**: Easy to upgrade resources
8. **Background Tasks**: Run cron jobs, daemons, etc.

## 🔧 Troubleshooting

### Service Won't Start
```bash
sudo journalctl -u domain-catcher -n 50
sudo systemctl status domain-catcher
```

### Permission Issues
```bash
sudo chown -R domaincatcher:domaincatcher /home/domaincatcher/DropCatchDomain
```

### Port Already in Use
```bash
sudo netstat -tlnp | grep :5000
sudo kill -9 PID
```

### Nginx Issues
```bash
sudo nginx -t
sudo systemctl status nginx
```

## 📈 Scaling Up

### Upgrade Linode Plan
1. Go to Linode dashboard
2. Click "Resize" on your instance
3. Choose larger plan
4. Reboot instance

### Add Load Balancer
- Use Linode NodeBalancer for high availability
- Configure multiple instances behind load balancer

### Database Upgrade
- Migrate from SQLite to PostgreSQL/MySQL
- Use Linode Managed Database service

## 🎯 Next Steps

1. **Deploy**: Follow the quick setup guide above
2. **Monitor**: Set up monitoring and alerts
3. **Backup**: Configure automated backups
4. **Scale**: Upgrade as your needs grow
5. **Optimize**: Fine-tune performance

Your domain monitoring system will now run 24/7 on your own Linode server with full control and access!
