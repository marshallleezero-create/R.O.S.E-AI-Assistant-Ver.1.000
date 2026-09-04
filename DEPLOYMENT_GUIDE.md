# 🚀 Documentation Deployment Guide

Deploy ROSE documentation to **AWS S3** (cloud-managed) or **self-hosted** (full control).

---

## Quick Start

### AWS S3 (5 minutes)
```bash
bash deploy-s3.sh rose-docs us-east-1
```

### Self-Hosted Docker (10 minutes)
```bash
bash deploy-self-hosted.sh rose-docs 80
```

---

## AWS S3 vs Self-Hosted Comparison

| Aspect | AWS S3 | Self-Hosted |
|--------|--------|-------------|
| **Setup Time** | 5 min | 10 min |
| **Monthly Cost** | $2-10 | $5-50 |
| **Maintenance** | AWS managed | Self-managed |
| **Scalability** | Unlimited | Limited by server |
| **CDN** | Optional CloudFront | Not included |
| **HTTPS** | AWS managed | Let's Encrypt |
| **Custom Domain** | ✅ Easy | ✅ Easy |
| **Full Control** | Limited | ✅ Full |
| **DevOps Knowledge** | Minimal | Moderate |

---

## AWS S3 Deployment

### When to Choose AWS S3

✅ Want **low maintenance**  
✅ Expect **high traffic**  
✅ Want **auto-scaling**  
✅ Prefer **managed service**  
✅ Need **global CDN**  

### Prerequisites

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# Enter: AWS Access Key ID
# Enter: AWS Secret Access Key
# Enter: Default region (us-east-1)
```

### Step-by-Step Deployment

```bash
# 1. Run automated deployment script
bash deploy-s3.sh

# OR manually:

# 1. Create S3 bucket
aws s3 mb s3://rose-docs --region us-east-1

# 2. Enable static website hosting
aws s3 website s3://rose-docs/ \
  --index-document index.html \
  --error-document index.html

# 3. Create and apply bucket policy
cat > policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicRead",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::rose-docs/*"
  }]
}
EOF
aws s3api put-bucket-policy --bucket rose-docs --policy file://policy.json

# 4. Build and upload documentation
mkdocs build
aws s3 sync site/ s3://rose-docs/ --delete

# Result: http://rose-docs.s3-website-us-east-1.amazonaws.com
```

### Add CloudFront CDN

```bash
# Create CloudFront distribution (via AWS Console)
# 1. Origin: S3 bucket
# 2. Default root object: index.html
# 3. Create SSL certificate (ACM)
# 4. Note CloudFront domain name
```

### Custom Domain with Route 53

```bash
# Create hosted zone for your domain
aws route53 create-hosted-zone --name docs.rose.com --caller-reference $(date +%s)

# Create alias record pointing to CloudFront
# (Use AWS Console for this)
# Result: https://docs.rose.com
```

### Costs Breakdown

| Item | Cost |
|------|------|
| S3 Storage (100MB) | $0.002/month |
| S3 Requests (1M/month) | $0.40/month |
| CloudFront (if used) | $0.085/GB |
| Route 53 (if used) | $0.50/month |
| **Total** | **$2-5/month** |

### Monitoring

```bash
# Check bucket size
aws s3api list-objects-v2 --bucket rose-docs \
  --query '[Contents[].Size] | sum(@)' --output text

# Check request count (CloudWatch)
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name NumberOfObjects \
  --dimensions Name=BucketName,Value=rose-docs \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-02-01T00:00:00Z \
  --period 86400 \
  --statistics Average
```

### CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Docs to S3

on:
  push:
    branches: [main]
    paths: ['docs/**', 'mkdocs.yml']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install mkdocs mkdocs-material
      - run: mkdocs build
      - uses: jakejarvis/s3-sync-action@master
        with:
          args: --delete
        env:
          AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
          SOURCE_DIR: site
```

---

## Self-Hosted Deployment

### When to Choose Self-Hosted

✅ Want **full control**  
✅ Have **existing infrastructure**  
✅ Want to **save money**  
✅ Need **custom configuration**  
✅ Have **IT team support**  

### Prerequisites

```bash
# Docker required
curl -fsSL https://get.docker.com | sh

# OR install mkdocs locally
pip install mkdocs mkdocs-material
```

### Quick Deployment (Docker Compose)

```bash
# Build documentation
mkdocs build

# Deploy with single command
docker-compose -f docker-compose.docs.yml up -d

# Result: http://localhost
# Logs: docker-compose -f docker-compose.docs.yml logs -f
```

### Automated Deployment Script

```bash
# Run automated deployment
bash deploy-self-hosted.sh rose-docs 80

# Script will:
# 1. Build mkdocs documentation
# 2. Create Dockerfile and nginx.conf
# 3. Build Docker image
# 4. Start container
# 5. Verify deployment
```

### Manual Setup (Linux Server)

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Install Docker
curl -fsSL https://get.docker.com | sh

# 3. Clone repository
git clone https://github.com/your-org/rose.git
cd rose

# 4. Build documentation
pip install mkdocs mkdocs-material
mkdocs build

# 5. Copy Dockerfile and nginx.conf
# (Already included in repository)

# 6. Build and run
docker build -t rose-docs .
docker run -d -p 80:80 -p 443:443 rose-docs

# Result: http://your-server.com
```

### Enable HTTPS (Let's Encrypt)

```bash
# 1. Install certbot
apt-get install certbot python3-certbot-nginx

# 2. Get certificate
certbot certonly --nginx -d docs.rose.com

# 3. Update nginx to use certificate
# (Update nginx.conf with SSL paths)

# 4. Rebuild Docker image
docker build -t rose-docs .
docker run -d -p 80:80 -p 443:443 -v /etc/letsencrypt:/etc/nginx/ssl rose-docs

# 5. Auto-renewal
systemctl enable certbot.timer
```

### Nginx Configuration

The included `nginx.conf` provides:

- ✅ Gzip compression
- ✅ Static asset caching (1 year for .js/.css)
- ✅ HTML cache control (1 hour)
- ✅ Security headers (X-Frame-Options, CSP, etc.)
- ✅ SPA routing fallback
- ✅ Deny access to hidden files
- ✅ Performance optimization

### Scaling Self-Hosted

```yaml
# docker-compose-prod.yml for multiple replicas
version: '3.8'

services:
  nginx-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - docs-1
      - docs-2
      - docs-3

  docs-1:
    image: rose-docs
    expose:
      - "80"

  docs-2:
    image: rose-docs
    expose:
      - "80"

  docs-3:
    image: rose-docs
    expose:
      - "80"
```

### Monitoring Self-Hosted

```bash
# View logs
docker logs -f rose-docs

# Monitor resources
docker stats rose-docs

# Health check
curl -v http://localhost/

# Restart if needed
docker restart rose-docs
```

### Costs Breakdown

| Item | Cost |
|------|------|
| VPS (1GB RAM) | $5-20/month |
| Domain name | $10-15/year |
| SSL certificate | Free (Let's Encrypt) |
| Bandwidth | Included in VPS |
| **Total** | **$5-20/month** |

### Backup Strategy

```bash
# Backup documentation files
docker cp rose-docs:/usr/share/nginx/html ./backup/

# Backup configuration
cp nginx.conf ./backup/
cp Dockerfile ./backup/

# Restore from backup
docker cp ./backup/html/. rose-docs:/usr/share/nginx/html/
docker restart rose-docs
```

---

## Deployment Comparison Table

### Performance
| Metric | AWS S3 | Self-Hosted |
|--------|--------|-------------|
| **Initial Response** | <100ms (CDN) | 50-500ms |
| **Bandwidth** | Unlimited | Server limited |
| **Concurrent Users** | Unlimited | ~1000s |
| **Failover** | Auto | Manual |

### Cost (Annual)
| Usage | AWS S3 | Self-Hosted |
|-------|--------|-------------|
| **Light** (10K req/mo) | $24 | $60 |
| **Medium** (1M req/mo) | $120 | $60 |
| **Heavy** (10M req/mo) | $600 | $120 |

### Maintenance
| Task | AWS S3 | Self-Hosted |
|------|--------|-------------|
| **Deployment** | Script | Script |
| **HTTPS** | Auto | Certbot |
| **Backups** | S3 versioning | Manual |
| **Monitoring** | CloudWatch | Docker logs |
| **Scaling** | Auto | Manual |

---

## Hybrid Approach

Use **both** for maximum resilience:

```bash
# Primary: AWS S3 + CloudFront (CDN)
# Fallback: Self-hosted Docker (backup)

# GitHub Actions deployer
deploy_to_s3()
deploy_to_self_hosted()
```

---

## Troubleshooting

### AWS S3

**Access Denied**
```bash
aws s3api get-bucket-policy --bucket rose-docs
aws s3api get-bucket-acl --bucket rose-docs
```

**Site not found**
```bash
aws s3api get-bucket-website --bucket rose-docs
aws s3 ls s3://rose-docs/
```

**High costs**
```bash
# Enable CloudFront to reduce S3 requests
# Set lifecycle rules to archive old versions
# Use S3 Intelligent-Tiering
```

### Self-Hosted

**Container won't start**
```bash
docker logs rose-docs
docker ps -a
docker inspect rose-docs
```

**Port already in use**
```bash
sudo lsof -i :80
sudo kill -9 <PID>
# OR use different port: docker run -p 8000:80
```

**Out of memory**
```bash
docker stats rose-docs
# Limit memory: docker run -m 512m rose-docs
```

**SSL certificate issues**
```bash
certbot renew --dry-run
certbot delete --cert-name docs.rose.com
certbot certonly --nginx -d docs.rose.com
```

---

## Next Steps

### Immediate (Pick One)

```bash
# AWS S3
bash deploy-s3.sh rose-docs us-east-1

# OR Self-Hosted
bash deploy-self-hosted.sh rose-docs 80
```

### Following (Recommended)

1. ✅ Test deployment in browser
2. ✅ Set up custom domain
3. ✅ Enable HTTPS/SSL
4. ✅ Set up automated backups
5. ✅ Configure CI/CD pipeline
6. ✅ Monitor traffic and performance
7. ✅ Plan scaling strategy

---

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [AWS S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

---

**Last Updated:** 2026-09-04  
**Version:** 1.0.0
