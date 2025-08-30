# 🚀 LuckyClub Setup Commands

## 📁 Create Static Assets Folders
```bash
mkdir -p static/{css,js,images,fonts}
mkdir -p static/css
mkdir -p static/js  
mkdir -p static/images
mkdir -p static/fonts
```

## 🔧 Install Dependencies
```bash
# Activate virtual environment
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Install additional packages if needed
pip install email-validator
```

## 🗄️ Database Setup
```bash
# Create database (if not already done)
sudo -u postgres psql <<'SQL'
CREATE DATABASE luckyclub;
CREATE USER luckyclub WITH PASSWORD 'Securepass1';
GRANT ALL PRIVILEGES ON DATABASE luckyclub TO luckyclub;
ALTER DATABASE luckyclub OWNER TO luckyclub;
SQL

# Run database migrations
alembic upgrade head
```

## 🚀 Test Application
```bash
# Test the application locally
python -m app.main

# Or run with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 9177 --reload
```

## ⚙️ Systemd Service Setup
```bash
# Copy service file to systemd directory
sudo cp luckyclub.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable luckyclub.service

# Start the service
sudo systemctl start luckyclub.service

# Check service status
sudo systemctl status luckyclub.service

# View logs
sudo journalctl -u luckyclub.service -f
```

## 🔍 Service Management Commands
```bash
# Start service
sudo systemctl start luckyclub.service

# Stop service
sudo systemctl stop luckyclub.service

# Restart service
sudo systemctl restart luckyclub.service

# Reload service (for config changes)
sudo systemctl reload luckyclub.service

# Check status
sudo systemctl status luckyclub.service

# View logs
sudo journalctl -u luckyclub.service

# Follow logs in real-time
sudo journalctl -u luckyclub.service -f

# View last 50 log entries
sudo journalctl -u luckyclub.service -n 50
```

## 🌐 Nginx Setup (Optional)
```bash
# Install Nginx
sudo apt update
sudo apt install nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/luckyclub

# Enable site
sudo ln -s /etc/nginx/sites-available/luckyclub /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 🔐 Firewall Setup
```bash
# Allow port 9177 (if not using Nginx)
sudo ufw allow 9177

# Allow port 80 (HTTP)
sudo ufw allow 80

# Allow port 443 (HTTPS)
sudo ufw allow 443

# Check firewall status
sudo ufw status
```

## 📊 Monitoring Commands
```bash
# Check if port is listening
sudo netstat -tlnp | grep 9177

# Check process
ps aux | grep uvicorn

# Check disk space
df -h

# Check memory usage
free -h

# Check system load
uptime
```

## 🗑️ Cleanup Commands
```bash
# Stop and disable service
sudo systemctl stop luckyclub.service
sudo systemctl disable luckyclub.service

# Remove service file
sudo rm /etc/systemd/system/luckyclub.service

# Reload systemd
sudo systemctl daemon-reload

# Reset systemd units
sudo systemctl reset-failed
```

## 🔄 Development Commands
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
alembic history
```

## 📝 Log Locations
```bash
# Systemd logs
sudo journalctl -u luckyclub.service

# Nginx logs (if using)
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs (if configured)
tail -f /var/log/luckyclub/app.log
```

## 🚨 Troubleshooting Commands
```bash
# Check service dependencies
sudo systemctl list-dependencies luckyclub.service

# Check service configuration
sudo systemctl cat luckyclub.service

# Check service environment
sudo systemctl show luckyclub.service

# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connection
psql -h localhost -U luckyclub -d luckyclub -c "SELECT version();"
```

## 📋 Quick Status Check
```bash
# One-liner to check everything
echo "=== LuckyClub Status ===" && \
echo "Service:" && sudo systemctl is-active luckyclub.service && \
echo "Port:" && sudo netstat -tlnp | grep 9177 && \
echo "Database:" && sudo systemctl is-active postgresql && \
echo "Logs:" && sudo journalctl -u luckyclub.service --no-pager -n 5
```
