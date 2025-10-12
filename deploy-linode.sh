#!/bin/bash

# Domain Catcher Linode Deployment Script
# This script automates the deployment of the domain monitoring system on Linode

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_USER="domaincatcher"
APP_DIR="/home/$APP_USER/DropCatchDomain"
SERVICE_NAME="domain-catcher"
NGINX_SITE="domain-catcher"

echo -e "${BLUE}🚀 Domain Catcher Linode Deployment Script${NC}"
echo "================================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   echo "Usage: sudo ./deploy-linode.sh"
   exit 1
fi

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Update system
echo -e "${BLUE}📦 Updating system packages...${NC}"
apt update && apt upgrade -y
print_status "System updated"

# Install required packages
echo -e "${BLUE}📦 Installing required packages...${NC}"
apt install -y python3 python3-pip python3-venv nginx git ufw curl
print_status "Required packages installed"

# Create application user
echo -e "${BLUE}👤 Creating application user...${NC}"
if ! id "$APP_USER" &>/dev/null; then
    adduser --disabled-password --gecos "" "$APP_USER"
    usermod -aG sudo "$APP_USER"
    print_status "User $APP_USER created"
else
    print_warning "User $APP_USER already exists"
fi

# Setup application directory
echo -e "${BLUE}📁 Setting up application directory...${NC}"
if [ ! -d "$APP_DIR" ]; then
    # If repository doesn't exist, we'll need to clone it
    print_warning "Application directory not found. Please clone your repository first:"
    echo "su - $APP_USER"
    echo "git clone https://github.com/YOUR_USERNAME/DropCatchDomain.git"
    echo "cd $APP_DIR"
    echo "Then run this script again."
    exit 1
fi

# Set ownership
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
print_status "Application directory ownership set"

# Create virtual environment
echo -e "${BLUE}🐍 Setting up Python virtual environment...${NC}"
sudo -u "$APP_USER" bash -c "
    cd $APP_DIR
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
"
print_status "Virtual environment created and dependencies installed"

# Create environment file if it doesn't exist
if [ ! -f "$APP_DIR/.env" ]; then
    echo -e "${BLUE}📝 Creating environment file...${NC}"
    sudo -u "$APP_USER" bash -c "
        cd $APP_DIR
        cat > .env << 'EOF'
# Domain Catcher Environment Configuration
DYNADOT_API_KEY=your_dynadot_api_key_here
PORKBUN_API_KEY=your_porkbun_api_key_here
PORKBUN_SECRET_KEY=your_porkbun_secret_key_here
DISCORD_WEBHOOK=your_discord_webhook_url_here
LOG_LEVEL=INFO
EOF
    "
    print_warning "Environment file created. Please edit $APP_DIR/.env with your API keys"
fi

# Install systemd service
echo -e "${BLUE}⚙️  Installing systemd service...${NC}"
cp "$APP_DIR/domain-catcher.service" "/etc/systemd/system/$SERVICE_NAME.service"

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
print_status "Systemd service installed and enabled"

# Configure nginx
echo -e "${BLUE}🌐 Configuring nginx...${NC}"
cp "$APP_DIR/nginx-domain-catcher.conf" "/etc/nginx/sites-available/$NGINX_SITE"

# Enable site
ln -sf "/etc/nginx/sites-available/$NGINX_SITE" "/etc/nginx/sites-enabled/"

# Remove default nginx site
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t
print_status "Nginx configuration validated"

# Setup firewall
echo -e "${BLUE}🔥 Configuring firewall...${NC}"
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80
ufw allow 443
print_status "Firewall configured"

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}"
systemctl start nginx
systemctl start "$SERVICE_NAME"

# Check service status
echo -e "${BLUE}📊 Checking service status...${NC}"
sleep 5

if systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_error "Nginx failed to start"
    systemctl status nginx
fi

if systemctl is-active --quiet "$SERVICE_NAME"; then
    print_status "Domain Catcher service is running"
else
    print_error "Domain Catcher service failed to start"
    systemctl status "$SERVICE_NAME"
fi

# Display final information
echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo "================================================"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Edit environment variables: nano $APP_DIR/.env"
echo "2. Restart service: systemctl restart $SERVICE_NAME"
echo "3. Check logs: journalctl -u $SERVICE_NAME -f"
echo "4. Test health endpoint: curl http://localhost/health"
echo ""
echo -e "${BLUE}🔧 Management Commands:${NC}"
echo "• Check status: systemctl status $SERVICE_NAME"
echo "• View logs: journalctl -u $SERVICE_NAME -f"
echo "• Restart: systemctl restart $SERVICE_NAME"
echo "• Stop: systemctl stop $SERVICE_NAME"
echo "• Start: systemctl start $SERVICE_NAME"
echo ""
echo -e "${BLUE}🌐 Access Information:${NC}"
echo "• Health Check: http://$(curl -s ifconfig.me)/health"
echo "• Application: http://$(curl -s ifconfig.me)/"
echo ""
echo -e "${YELLOW}⚠️  Important:${NC}"
echo "• Make sure to configure your API keys in $APP_DIR/.env"
echo "• Consider setting up SSL with Let's Encrypt"
echo "• Monitor your Linode usage and costs"
echo ""
echo -e "${GREEN}✅ Your domain monitoring system is now running on Linode!${NC}"
