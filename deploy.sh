#!/bin/bash

#############################################
# SQL Query Buddy - Quick Deployment Script
#############################################

set -e  # Exit on error

echo "=================================="
echo "SQL Query Buddy Deployment Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Error: This script should not be run as root${NC}"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print step
print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

# Function to print error
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check system requirements
print_step "Checking system requirements..."

if ! command_exists python3; then
    print_error "Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    print_error "Node.js is not installed"
    exit 1
fi

if ! command_exists redis-server; then
    print_warning "Redis is not installed. Installing..."
    sudo apt update
    sudo apt install -y redis-server
fi

echo -e "${GREEN}✓${NC} System requirements met"
echo ""

# Ask deployment method
echo "Choose deployment method:"
echo "1) Docker (Recommended)"
echo "2) Manual (Systemd services)"
echo ""
read -p "Enter choice [1-2]: " deploy_choice

case $deploy_choice in
    1)
        print_step "Deploying with Docker..."

        # Check if Docker is installed
        if ! command_exists docker; then
            print_error "Docker is not installed"
            echo "Install Docker with: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
            exit 1
        fi

        if ! command_exists docker-compose; then
            print_error "Docker Compose is not installed"
            exit 1
        fi

        # Check for .env file
        if [ ! -f .env ]; then
            print_warning ".env file not found. Creating from template..."
            cp .env.example .env 2>/dev/null || cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
REDIS_HOST=redis
REDIS_PORT=6379
ENVIRONMENT=production
EOF
            echo -e "${YELLOW}Please edit .env file and add your OpenAI API key${NC}"
            read -p "Press Enter when ready to continue..."
        fi

        # Build and start containers
        print_step "Building Docker images..."
        docker-compose build

        print_step "Starting containers..."
        docker-compose up -d

        print_step "Waiting for services to start..."
        sleep 10

        # Initialize vector database
        print_step "Initializing vector database..."
        docker-compose exec backend python backend/rag/embed_schema.py

        echo ""
        echo -e "${GREEN}=================================="
        echo "Deployment Complete!"
        echo "==================================${NC}"
        echo ""
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
        echo "API Docs: http://localhost:8000/docs"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop services: docker-compose down"
        ;;

    2)
        print_step "Manual deployment selected..."

        # Setup Python virtual environment
        print_step "Setting up Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate

        # Install Python dependencies
        print_step "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt

        # Check for .env file
        if [ ! -f .env ]; then
            print_warning ".env file not found. Creating from template..."
            cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
ENVIRONMENT=production
EOF
            echo -e "${YELLOW}Please edit .env file and add your OpenAI API key${NC}"
            read -p "Press Enter when ready to continue..."
        fi

        # Initialize vector database
        print_step "Initializing vector database..."
        python backend/rag/embed_schema.py

        # Setup frontend
        print_step "Setting up frontend..."
        cd frontend
        npm install
        npm run build
        cd ..

        # Start Redis
        print_step "Starting Redis..."
        sudo systemctl start redis-server
        sudo systemctl enable redis-server

        # Ask if user wants to setup systemd services
        read -p "Setup systemd services? (y/n): " setup_systemd

        if [[ $setup_systemd == "y" ]]; then
            print_step "Setting up systemd services..."

            # Create backend service
            sudo tee /etc/systemd/system/sqlbuddy-backend.service > /dev/null << EOF
[Unit]
Description=SQL Query Buddy Backend
After=network.target redis-server.service

[Service]
Type=notify
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
EnvironmentFile=$(pwd)/.env
ExecStart=$(pwd)/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
EOF

            sudo systemctl daemon-reload
            sudo systemctl enable sqlbuddy-backend
            sudo systemctl start sqlbuddy-backend

            echo ""
            echo -e "${GREEN}Systemd services configured!${NC}"
            echo "Backend service: sqlbuddy-backend"
            echo ""
            echo "Commands:"
            echo "  sudo systemctl status sqlbuddy-backend"
            echo "  sudo systemctl restart sqlbuddy-backend"
            echo "  journalctl -u sqlbuddy-backend -f"
        else
            print_step "Starting backend manually..."
            echo ""
            echo "To start the backend, run:"
            echo "  source venv/bin/activate"
            echo "  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
            echo ""
            echo "To serve the frontend, run:"
            echo "  npx serve -s frontend/build -l 3000"
        fi

        echo ""
        echo -e "${GREEN}=================================="
        echo "Manual Deployment Complete!"
        echo "==================================${NC}"
        echo ""
        echo "Backend: http://localhost:8000"
        echo "Frontend: Serve the frontend/build directory"
        echo "API Docs: http://localhost:8000/docs"
        ;;

    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}For production deployment with Nginx, see VM_DEPLOYMENT_GUIDE.md${NC}"
