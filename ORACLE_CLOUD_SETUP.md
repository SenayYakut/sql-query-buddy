# Oracle Cloud Free Tier Deployment

Complete guide for deploying SQL Query Buddy on Oracle Cloud's **Always Free** tier.

---

## Why Oracle Cloud Free Tier?

✅ **Always Free** - No time limit, no credit card for free tier
✅ **Generous Resources** - 4 ARM cores + 24GB RAM
✅ **Perfect for Contests** - Deploy once, use forever
✅ **200GB Storage** - More than enough

---

## Step 1: Create Oracle Cloud Account

1. Go to: https://www.oracle.com/cloud/free/
2. Click **Start for free**
3. Fill in details (no credit card needed for Always Free)
4. Verify email
5. Login to Oracle Cloud Console

---

## Step 2: Create a Free VM Instance

### 1. Navigate to Compute Instances
- Click **☰ Menu** → **Compute** → **Instances**
- Click **Create Instance**

### 2. Configure Instance (Always Free Settings)

**Name:** `sqlbuddy-vm`

**Placement:**
- Leave default (Availability Domain)

**Image and Shape:**
- Click **Edit** → **Change Shape**
- Select **Ampere (ARM)** → **VM.Standard.A1.Flex**
- OCPUs: **2** (or up to 4 if available)
- Memory: **12 GB** (or up to 24 GB)
- Click **Change Image** → Select **Ubuntu 22.04 Minimal**

**Networking:**
- Use default VCN
- Assign a public IP: **Yes**

**Add SSH Keys:**
- Generate SSH key pair (or use existing)
- Select **Generate a key pair for me** → Download both keys
- OR **Upload public key** if you have one

**Boot Volume:**
- 50 GB (Always Free tier allows up to 200GB total)

Click **Create**

---

## Step 3: Configure Firewall Rules

### Open Required Ports

1. Click on your instance → **Virtual Cloud Network** → Click your VCN name
2. Click **Security Lists** → Click your security list
3. Click **Add Ingress Rules** and add:

**Rule 1: HTTP**
- Source CIDR: `0.0.0.0/0`
- Destination Port: `80`

**Rule 2: HTTPS**
- Source CIDR: `0.0.0.0/0`
- Destination Port: `443`

**Rule 3: Backend (Testing)**
- Source CIDR: `0.0.0.0/0`
- Destination Port: `8000`

4. Click **Add Ingress Rules**

### Configure Ubuntu Firewall

SSH into your instance:
```bash
# Use the private key you downloaded
chmod 400 ssh-key-*.key
ssh -i ssh-key-*.key ubuntu@<your-public-ip>
```

Once connected:
```bash
# Allow required ports
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo netfilter-persistent save
```

---

## Step 4: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Redis
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Install Git
sudo apt install -y git

# Install Nginx (optional, for production)
sudo apt install -y nginx
```

---

## Step 5: Deploy Application

### Clone Repository
```bash
cd ~
git clone https://github.com/yourusername/sql-query-buddy.git
cd sql-query-buddy
```

### Setup Backend
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your OpenAI API key
```

### Initialize Vector Database
```bash
source venv/bin/activate
python backend/rag/embed_schema.py
```

### Build Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## Step 6: Run Application

### Option A: Quick Start (Testing)

**Terminal 1 - Backend:**
```bash
cd ~/sql-query-buddy
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ~/sql-query-buddy/frontend
npx serve -s build -l 3000
```

Access at: `http://<your-public-ip>:8000` (backend) and `http://<your-public-ip>:3000` (frontend)

### Option B: Production with Systemd (Recommended)

**1. Create Backend Service:**
```bash
sudo tee /etc/systemd/system/sqlbuddy-backend.service > /dev/null << 'EOF'
[Unit]
Description=SQL Query Buddy Backend
After=network.target redis-server.service

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/sql-query-buddy
Environment="PATH=/home/ubuntu/sql-query-buddy/venv/bin"
EnvironmentFile=/home/ubuntu/sql-query-buddy/.env
ExecStart=/home/ubuntu/sql-query-buddy/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

**2. Start Backend:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable sqlbuddy-backend
sudo systemctl start sqlbuddy-backend
sudo systemctl status sqlbuddy-backend
```

**3. Configure Nginx:**
```bash
sudo tee /etc/nginx/sites-available/sqlbuddy > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root /home/ubuntu/sql-query-buddy/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /rag {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location ~ ^/(customers|orders|products) {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/sqlbuddy /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 7: Access Your Application

Your app is now live at:
- **Frontend:** `http://<your-public-ip>`
- **Backend API:** `http://<your-public-ip>/rag`
- **API Docs:** `http://<your-public-ip>:8000/docs`

Find your public IP:
```bash
curl ifconfig.me
```

---

## Cost: $0 Forever! 💰

This setup uses only Always Free resources:
- ✅ VM: Free (within Always Free limits)
- ✅ Storage: Free (up to 200GB)
- ✅ Network: Free (up to 10TB/month)
- ⚠️ **Only cost:** OpenAI API usage (pay per request)

---

## Troubleshooting

### Can't SSH into instance?
```bash
# Check if using correct key
chmod 400 ssh-key-*.key
ssh -i ssh-key-*.key ubuntu@<public-ip>

# Try with verbose mode
ssh -v -i ssh-key-*.key ubuntu@<public-ip>
```

### Ports not accessible?
```bash
# Check Oracle Cloud security rules (see Step 3)
# Check Ubuntu firewall
sudo iptables -L -n
```

### Backend not starting?
```bash
# Check logs
journalctl -u sqlbuddy-backend -f

# Check if Redis is running
sudo systemctl status redis-server

# Test manually
cd ~/sql-query-buddy
source venv/bin/activate
uvicorn backend.main:app --reload
```

### Out of memory?
```bash
# Create swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Monitoring

### Check Service Status
```bash
sudo systemctl status sqlbuddy-backend
sudo systemctl status nginx
sudo systemctl status redis-server
```

### View Logs
```bash
# Backend logs
journalctl -u sqlbuddy-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Monitor Resources
```bash
# Install htop
sudo apt install htop
htop

# Check disk
df -h

# Check memory
free -h
```

---

## Updating the Application

```bash
cd ~/sql-query-buddy
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
cd frontend && npm install && npm run build && cd ..
sudo systemctl restart sqlbuddy-backend
sudo systemctl reload nginx
```

---

## Security Recommendations

1. **Restrict SSH Access:**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

2. **Setup UFW Firewall:**
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

3. **Secure .env file:**
```bash
chmod 600 ~/sql-query-buddy/.env
```

4. **Regular Updates:**
```bash
sudo apt update && sudo apt upgrade -y
```

---

## Next Steps

- **Add Domain:** Point your domain to the public IP
- **Enable HTTPS:** Use Let's Encrypt with `certbot`
- **Monitor Usage:** Check Oracle Cloud usage dashboard
- **Backup:** Setup automated backups

---

## Performance Tips for ARM (Ampere A1)

ARM processors are very efficient! To maximize performance:

1. **Use all available cores:**
```bash
# Edit backend service, increase workers
sudo nano /etc/systemd/system/sqlbuddy-backend.service
# Change: --workers 4
sudo systemctl daemon-reload
sudo systemctl restart sqlbuddy-backend
```

2. **Optimize Redis:**
```bash
sudo nano /etc/redis/redis.conf
# Add:
maxmemory 2gb
maxmemory-policy allkeys-lru
sudo systemctl restart redis-server
```

---

**Deployment Complete!** 🎉

Your SQL Query Buddy is now running on Oracle Cloud's Always Free tier and will cost you $0 in infrastructure!
