# SQL Query Buddy - VM Deployment Guide

Complete guide for deploying SQL Query Buddy to a virtual machine (Ubuntu/Debian).

---

## Table of Contents
1. [VM Requirements](#vm-requirements)
2. [Initial Server Setup](#initial-server-setup)
3. [Install Dependencies](#install-dependencies)
4. [Project Setup](#project-setup)
5. [Configure Services](#configure-services)
6. [Deploy Backend](#deploy-backend)
7. [Deploy Frontend](#deploy-frontend)
8. [Setup Nginx Reverse Proxy](#setup-nginx-reverse-proxy)
9. [Enable Systemd Services](#enable-systemd-services)
10. [Security Hardening](#security-hardening)
11. [Monitoring & Logs](#monitoring--logs)

---

## VM Requirements

### Minimum Specifications
- **OS**: Ubuntu 22.04 LTS or Debian 11+
- **CPU**: 2 vCPUs
- **RAM**: 4 GB
- **Storage**: 20 GB SSD
- **Network**: Public IP with ports 80, 443 open

### Recommended Specifications
- **CPU**: 4 vCPUs
- **RAM**: 8 GB
- **Storage**: 40 GB SSD

---

## Initial Server Setup

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Create Application User
```bash
sudo adduser sqlbuddy --disabled-password --gecos ""
sudo usermod -aG sudo sqlbuddy
```

### 3. Setup Firewall
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. Set Timezone (Optional)
```bash
sudo timedatectl set-timezone America/New_York
```

---

## Install Dependencies

### 1. Install Python 3.11+
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

### 2. Install Node.js 18+
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node --version  # Should be v18+
npm --version
```

### 3. Install Redis
```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
redis-cli ping  # Should return PONG
```

### 4. Install Nginx
```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 5. Install Build Tools
```bash
sudo apt install -y build-essential git curl wget
```

---

## Project Setup

### 1. Clone Repository
```bash
cd /home/sqlbuddy
sudo -u sqlbuddy git clone https://github.com/yourusername/sql-query-buddy.git
cd sql-query-buddy
sudo chown -R sqlbuddy:sqlbuddy /home/sqlbuddy/sql-query-buddy
```

### 2. Backend Setup
```bash
# Switch to application user
sudo su - sqlbuddy
cd /home/sqlbuddy/sql-query-buddy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install fastapi uvicorn[standard] python-dotenv
pip install langchain langchain-openai langchain-community
pip install chromadb redis mem0ai qdrant-client
pip install openai tiktoken
pip install pydantic sqlalchemy
```

### 3. Create requirements.txt
```bash
cat > requirements.txt << 'EOF'
fastapi==0.115.12
uvicorn[standard]==0.38.0
python-dotenv==1.2.1
langchain==0.3.22
langchain-openai==0.3.12
langchain-community==0.4.1
chromadb==1.3.5
redis==5.2.4
mem0ai==1.1.6
qdrant-client==1.15.1
openai==2.8.0
tiktoken==0.12.0
pydantic==2.11.1
sqlalchemy==2.0.44
EOF

pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=info
EOF

chmod 600 .env
```

### 5. Initialize Vector Database
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Run schema embedding
python backend/rag/embed_schema.py
```

### 6. Frontend Setup
```bash
cd /home/sqlbuddy/sql-query-buddy/frontend

# Install dependencies
npm install

# Build for production
npm run build
```

---

## Configure Services

### 1. Create Backend Systemd Service
```bash
sudo tee /etc/systemd/system/sqlbuddy-backend.service > /dev/null << 'EOF'
[Unit]
Description=SQL Query Buddy Backend (FastAPI)
After=network.target redis-server.service
Requires=redis-server.service

[Service]
Type=notify
User=sqlbuddy
Group=sqlbuddy
WorkingDirectory=/home/sqlbuddy/sql-query-buddy
Environment="PATH=/home/sqlbuddy/sql-query-buddy/venv/bin"
EnvironmentFile=/home/sqlbuddy/sql-query-buddy/.env
ExecStart=/home/sqlbuddy/sql-query-buddy/venv/bin/uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### 2. Create Frontend Service (Optional - Using serve)
```bash
# Install serve globally
sudo npm install -g serve

sudo tee /etc/systemd/system/sqlbuddy-frontend.service > /dev/null << 'EOF'
[Unit]
Description=SQL Query Buddy Frontend (React)
After=network.target

[Service]
Type=simple
User=sqlbuddy
Group=sqlbuddy
WorkingDirectory=/home/sqlbuddy/sql-query-buddy/frontend
ExecStart=/usr/bin/serve -s build -l 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### 3. Configure Redis
```bash
sudo tee -a /etc/redis/redis.conf > /dev/null << 'EOF'

# SQL Query Buddy Configuration
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
EOF

sudo systemctl restart redis-server
```

---

## Deploy Backend

### 1. Start Backend Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable sqlbuddy-backend
sudo systemctl start sqlbuddy-backend
```

### 2. Check Backend Status
```bash
sudo systemctl status sqlbuddy-backend
journalctl -u sqlbuddy-backend -f
```

### 3. Test Backend
```bash
curl http://localhost:8000/customers
```

---

## Deploy Frontend

### Option 1: Using Nginx to Serve Static Files (Recommended)

The frontend build files will be served directly by Nginx (configured in next section).

### Option 2: Using serve with systemd

```bash
sudo systemctl daemon-reload
sudo systemctl enable sqlbuddy-frontend
sudo systemctl start sqlbuddy-frontend
sudo systemctl status sqlbuddy-frontend
```

---

## Setup Nginx Reverse Proxy

### 1. Create Nginx Configuration
```bash
sudo tee /etc/nginx/sites-available/sqlbuddy > /dev/null << 'EOF'
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or IP

    client_max_body_size 10M;

    # Frontend - Serve static files
    location / {
        root /home/sqlbuddy/sql-query-buddy/frontend/build;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /rag {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts for long-running queries
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Additional backend endpoints
    location ~ ^/(customers|orders|products) {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF
```

### 2. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/sqlbuddy /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Setup SSL with Let's Encrypt (Optional but Recommended)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

The Nginx configuration will be automatically updated for HTTPS.

---

## Enable Systemd Services

### Start All Services
```bash
sudo systemctl enable redis-server
sudo systemctl enable sqlbuddy-backend
sudo systemctl enable nginx

sudo systemctl start redis-server
sudo systemctl start sqlbuddy-backend
sudo systemctl start nginx
```

### Check Status
```bash
sudo systemctl status redis-server
sudo systemctl status sqlbuddy-backend
sudo systemctl status nginx
```

---

## Security Hardening

### 1. Configure Firewall
```bash
sudo ufw status
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. Secure Redis
```bash
sudo tee -a /etc/redis/redis.conf > /dev/null << 'EOF'
bind 127.0.0.1
requirepass your_secure_redis_password_here
EOF

sudo systemctl restart redis-server
```

Update `.env`:
```bash
REDIS_PASSWORD=your_secure_redis_password_here
```

### 3. Secure Environment File
```bash
sudo chmod 600 /home/sqlbuddy/sql-query-buddy/.env
sudo chown sqlbuddy:sqlbuddy /home/sqlbuddy/sql-query-buddy/.env
```

### 4. Update CORS in Production
Edit `/home/sqlbuddy/sql-query-buddy/backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Replace with your domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

Then restart backend:
```bash
sudo systemctl restart sqlbuddy-backend
```

### 5. Regular Updates
```bash
# Create update script
cat > /home/sqlbuddy/update.sh << 'EOF'
#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
EOF

chmod +x /home/sqlbuddy/update.sh

# Setup cron job for weekly updates
(crontab -l 2>/dev/null; echo "0 3 * * 0 /home/sqlbuddy/update.sh") | crontab -
```

---

## Monitoring & Logs

### 1. View Logs
```bash
# Backend logs
journalctl -u sqlbuddy-backend -f

# Nginx access logs
tail -f /var/log/nginx/access.log

# Nginx error logs
tail -f /var/log/nginx/error.log

# Redis logs
tail -f /var/log/redis/redis-server.log
```

### 2. Check Service Status
```bash
systemctl status sqlbuddy-backend
systemctl status nginx
systemctl status redis-server
```

### 3. Monitor Resources
```bash
# Install htop
sudo apt install -y htop

# Monitor system resources
htop

# Check disk usage
df -h

# Check memory usage
free -h
```

### 4. Setup Log Rotation
```bash
sudo tee /etc/logrotate.d/sqlbuddy > /dev/null << 'EOF'
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
EOF
```

---

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
journalctl -u sqlbuddy-backend -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000

# Manually test backend
sudo su - sqlbuddy
cd /home/sqlbuddy/sql-query-buddy
source venv/bin/activate
uvicorn backend.main:app --reload
```

### Frontend Not Loading
```bash
# Check Nginx configuration
sudo nginx -t

# Check if build exists
ls -la /home/sqlbuddy/sql-query-buddy/frontend/build

# Rebuild if needed
cd /home/sqlbuddy/sql-query-buddy/frontend
npm run build
```

### Redis Connection Issues
```bash
# Test Redis
redis-cli ping

# Check Redis service
sudo systemctl status redis-server

# View Redis logs
tail -f /var/log/redis/redis-server.log
```

### Qdrant/Mem0 Issues
```bash
# Check if Qdrant storage directory exists
ls -la /home/sqlbuddy/sql-query-buddy/qdrant_storage

# Re-run embedding if needed
cd /home/sqlbuddy/sql-query-buddy
source venv/bin/activate
python backend/rag/embed_schema.py
```

---

## Updating the Application

### 1. Pull Latest Code
```bash
sudo su - sqlbuddy
cd /home/sqlbuddy/sql-query-buddy
git pull origin main
```

### 2. Update Backend
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart sqlbuddy-backend
```

### 3. Update Frontend
```bash
cd frontend
npm install
npm run build
sudo systemctl reload nginx
```

### 4. Verify Deployment
```bash
curl http://localhost:8000/customers
curl http://your-domain.com
```

---

## Backup & Restore

### Backup Script
```bash
cat > /home/sqlbuddy/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/sqlbuddy/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
cp /home/sqlbuddy/sql-query-buddy/backend/db/retail.db $BACKUP_DIR/retail_$DATE.db

# Backup vector stores
tar -czf $BACKUP_DIR/vectorstores_$DATE.tar.gz \
    /home/sqlbuddy/sql-query-buddy/backend/rag/vectorstore \
    /home/sqlbuddy/sql-query-buddy/qdrant_storage

# Backup environment file
cp /home/sqlbuddy/sql-query-buddy/.env $BACKUP_DIR/.env_$DATE

# Keep only last 7 backups
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /home/sqlbuddy/backup.sh

# Setup daily backup cron
(crontab -l 2>/dev/null; echo "0 2 * * * /home/sqlbuddy/backup.sh") | crontab -
```

---

## Performance Optimization

### 1. Increase Uvicorn Workers
Edit `/etc/systemd/system/sqlbuddy-backend.service`:
```
--workers 8  # Based on CPU cores
```

### 2. Enable Nginx Caching
Add to Nginx config:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;

location /rag {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    # ... rest of proxy config
}
```

### 3. Optimize Redis
```bash
# Add to /etc/redis/redis.conf
maxmemory 1gb
maxmemory-policy allkeys-lru
tcp-backlog 511
```

---

## Quick Reference

### Service Commands
```bash
# Restart backend
sudo systemctl restart sqlbuddy-backend

# Reload Nginx
sudo systemctl reload nginx

# Restart Redis
sudo systemctl restart redis-server

# View all service statuses
sudo systemctl status sqlbuddy-backend nginx redis-server
```

### Log Commands
```bash
# Backend logs (live)
journalctl -u sqlbuddy-backend -f

# Nginx access log
tail -f /var/log/nginx/access.log

# All logs
journalctl -xe
```

---

## Contact & Support

For issues and support:
- GitHub Issues: [Your Repo URL]
- Documentation: [README.md](README.md)

---

**Deployment Complete!** Your SQL Query Buddy should now be accessible at `http://your-domain.com`
