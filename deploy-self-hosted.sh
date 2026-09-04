#!/bin/bash

# ROSE Documentation Self-Hosted Deployment
# Script to build and deploy MkDocs documentation with Docker

set -e

# Configuration
CONTAINER_NAME="${1:-rose-docs}"
PORT="${2:-80}"
IMAGE_NAME="rose-docs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 ROSE Documentation Self-Hosted Deployment${NC}\n"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v mkdocs &> /dev/null; then
    echo -e "${RED}❌ mkdocs not found. Install: pip install mkdocs mkdocs-material${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Install Docker: https://docker.com${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}\n"

# Build documentation
echo -e "${YELLOW}🔨 Building documentation...${NC}"
mkdocs build --quiet
echo -e "${GREEN}✅ Documentation built${NC}\n"

# Create Dockerfile
echo -e "${YELLOW}📝 Creating Dockerfile...${NC}"
cat > Dockerfile << 'EOF'
FROM nginx:alpine

# Copy built documentation
COPY site/ /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
EOF
echo -e "${GREEN}✅ Dockerfile created${NC}\n"

# Create nginx.conf
echo -e "${YELLOW}📝 Creating nginx.conf...${NC}"
cat > nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml text/javascript 
               application/x-javascript application/xml+rss 
               application/json application/javascript;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html index.htm;

        # SPA fallback - route non-existent paths to index.html
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Cache static assets for 1 year
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Don't cache HTML files
        location ~* \.html?$ {
            expires 1h;
            add_header Cache-Control "public, must-revalidate";
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

        # Deny access to sensitive files
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }

        location ~ ~$ {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
EOF
echo -e "${GREEN}✅ nginx.conf created${NC}\n"

# Stop existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}⏹️  Stopping existing container...${NC}"
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# Build Docker image
echo -e "${YELLOW}🏗️  Building Docker image...${NC}"
docker build -t "$IMAGE_NAME" -q .
echo -e "${GREEN}✅ Docker image built${NC}\n"

# Run container
echo -e "${YELLOW}🚀 Starting container...${NC}"
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p "$PORT:80" \
    "$IMAGE_NAME"

# Wait for container to be healthy
echo -e "${YELLOW}⏳ Waiting for container to be ready...${NC}"
sleep 2

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${GREEN}✅ Container is running${NC}\n"
else
    echo -e "${RED}❌ Container failed to start${NC}"
    docker logs "$CONTAINER_NAME"
    exit 1
fi

# Test deployment
echo -e "${YELLOW}🧪 Testing deployment...${NC}"
if curl -s "http://localhost:$PORT/" > /dev/null; then
    echo -e "${GREEN}✅ Documentation is accessible${NC}\n"
else
    echo -e "${YELLOW}⚠️  Could not connect, but container is running${NC}\n"
fi

# Display information
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "📍 ${YELLOW}Documentation URL:${NC}"
echo "   http://localhost:$PORT"
echo ""
echo -e "🐳 ${YELLOW}Container Name:${NC} $CONTAINER_NAME"
echo -e "🖼️  ${YELLOW}Image Name:${NC} $IMAGE_NAME"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  View logs:           docker logs -f $CONTAINER_NAME"
echo "  Stop container:      docker stop $CONTAINER_NAME"
echo "  Start container:     docker start $CONTAINER_NAME"
echo "  Remove container:    docker rm $CONTAINER_NAME"
echo "  Open in browser:     open http://localhost:$PORT"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Open http://localhost:$PORT in your browser"
echo "  2. Configure HTTPS with nginx and Let's Encrypt"
echo "  3. Deploy to production server with Docker Compose"
echo ""

exit 0
