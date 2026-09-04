#!/bin/bash

# ROSE Documentation Deployment to AWS S3
# Script to build and upload MkDocs documentation to AWS S3

set -e  # Exit on error

# Configuration
BUCKET_NAME="${1:-rose-docs}"
AWS_REGION="${2:-us-east-1}"
PROFILE="${3:-default}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 ROSE Documentation Deployment to AWS S3${NC}\n"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v mkdocs &> /dev/null; then
    echo -e "${RED}❌ mkdocs not found. Install: pip install mkdocs mkdocs-material${NC}"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Install: pip install awscli${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}\n"

# Build documentation
echo -e "${YELLOW}🔨 Building documentation...${NC}"
mkdocs build --quiet
echo -e "${GREEN}✅ Documentation built${NC}\n"

# Verify S3 bucket exists
echo -e "${YELLOW}🔍 Checking S3 bucket...${NC}"
if ! aws s3 ls "s3://$BUCKET_NAME" --profile "$PROFILE" 2>&1 | grep -q .; then
    echo -e "${RED}❌ Bucket '$BUCKET_NAME' not found or not accessible${NC}"
    echo -e "${YELLOW}Creating bucket...${NC}"
    aws s3 mb "s3://$BUCKET_NAME" --region "$AWS_REGION" --profile "$PROFILE"
    
    echo -e "${YELLOW}Enabling static website hosting...${NC}"
    aws s3 website "s3://$BUCKET_NAME/" \
        --index-document index.html \
        --error-document index.html \
        --profile "$PROFILE"
    
    echo -e "${YELLOW}Setting bucket policy...${NC}"
    cat > /tmp/bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
  }]
}
EOF
    aws s3api put-bucket-policy \
        --bucket "$BUCKET_NAME" \
        --policy "file:///tmp/bucket-policy.json" \
        --profile "$PROFILE"
    rm /tmp/bucket-policy.json
fi

echo -e "${GREEN}✅ Bucket verified${NC}\n"

# Upload documentation
echo -e "${YELLOW}📤 Uploading documentation to S3...${NC}"
aws s3 sync site/ "s3://$BUCKET_NAME/" \
    --delete \
    --region "$AWS_REGION" \
    --profile "$PROFILE" \
    --metadata-directive REPLACE \
    --cache-control "max-age=3600" \
    --exclude "*.map" \
    --exclude ".git*"

echo -e "${GREEN}✅ Documentation uploaded${NC}\n"

# Display deployment information
WEBSITE_URL="http://$BUCKET_NAME.s3-website-$AWS_REGION.amazonaws.com"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "📍 ${YELLOW}Documentation URL:${NC}"
echo "   $WEBSITE_URL"
echo ""
echo -e "📦 ${YELLOW}Bucket Name:${NC} $BUCKET_NAME"
echo -e "🌍 ${YELLOW}Region:${NC} $AWS_REGION"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Test the documentation: curl '$WEBSITE_URL'"
echo "  2. To use a custom domain, configure Route 53"
echo "  3. To enable CloudFront CDN, create a distribution"
echo ""

exit 0
