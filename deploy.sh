#!/bin/bash

# Quick deployment script for Optibot
# This script automates the entire deployment process

set -e

echo "🚀 Optibot Deployment Script"
echo "=============================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform is required but not installed."; exit 1; }
command -v az >/dev/null 2>&1 || { echo "❌ Azure CLI is required but not installed."; exit 1; }

echo "✅ All prerequisites met"

# Step 1: Build and push Docker image
echo ""
echo "📦 Step 1: Building Docker image..."
docker build -t optibot-assistant .

echo "🔐 Logging into GitHub Container Registry..."
echo "Please enter your GitHub Personal Access Token:"
read -s GH_TOKEN
echo "$GH_TOKEN" | docker login ghcr.io -u mahara0511 --password-stdin

echo "⬆️  Pushing image to GHCR..."
docker tag optibot-assistant ghcr.io/mahara0511/nguyenminhkhanhtest:latest
docker push ghcr.io/mahara0511/nguyenminhkhanhtest:latest

echo "✅ Docker image pushed successfully"

# Step 2: Deploy infrastructure with Terraform
echo ""
echo "🏗️  Step 2: Deploying Azure infrastructure..."
cd infra

if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found. Please create it from terraform.tfvars.example"
    exit 1
fi

terraform init
terraform plan -out=tfplan
echo ""
echo "⚠️  About to create Azure resources. Continue? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    terraform apply tfplan
    echo "✅ Infrastructure deployed"
    
    # Get outputs
    VM_IP=$(terraform output -raw public_ip_address)
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================="
    echo "VM IP: $VM_IP"
    echo "API URL: http://$VM_IP:8000"
    echo "Swagger UI: http://$VM_IP:8000/docs"
    echo ""
    echo "⏳ Wait 2-3 minutes for VM initialization to complete"
    echo "📝 Daily scraper runs at 2:00 AM daily"
    echo "📊 View logs: ssh azureuser@$VM_IP 'tail -f /var/log/optibot/scraper.log'"
else
    echo "❌ Deployment cancelled"
    exit 1
fi

cd ..
