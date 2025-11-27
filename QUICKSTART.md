# Quick Start Guide

## Goal

Deploy an AI chatbot assistant with automated daily data scraping on Azure VM using Docker, Terraform, and CI/CD.

## 5-Minute Local Test

```bash
# 1. Setup
cp .env.sample .env
# Edit .env and add your GEMINI_API_KEY

# 2. Run with Docker
docker build -t optibot-assistant .
docker run --rm -p 8000:8000 \
  -e GEMINI_API_KEY="your_key" \
  -v $(pwd)/chroma_storage:/app/chroma_storage \
  optibot-assistant

# 3. Test
# Open: http://localhost:8000/docs
# Or: curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"What is Optisigns?"}'
```

## Deploy to Azure (Automated)

```bash
# 1. Configure Terraform
cd infra
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 2. Run deployment script
cd ..
./deploy.sh
```

The script will:

- Build & push Docker image to GHCR
- Create Azure VM with Terraform
- Setup Docker, pull image, run API
- Configure daily cron job (2 AM)

## 📊 What the Daily Job Does

1. **Re-scrapes** all articles from Optisigns support API
2. **Computes hash** (SHA256) of each article
3. **Detects changes**:
   - Added: New articles
   - Updated: Changed content
   - Skipped: Unchanged
4. **Updates** ChromaDB with only added/updated articles
5. **Logs** results: `/var/log/optibot/scraper.log`

## 🔍 Monitoring

```bash
# SSH to VM
ssh azureuser@YOUR_VM_IP

# View API logs
docker logs -f optibot-api

# View scraper logs
tail -f /var/log/optibot/scraper.log

# Check last run summary
cat /var/log/optibot/scraper.log | grep "DAILY JOB RESULT" -A 3
```

## 🎯 CI/CD

Every push to `main` branch:

1. GitHub Actions builds image
2. Pushes to GHCR
3. SSHs to VM and redeploys

Setup GitHub Secrets:

- `AZURE_VM_HOST`
- `AZURE_VM_USER`
- `AZURE_VM_SSH_KEY`
- `GEMINI_API_KEY`

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

## 🆘 Troubleshooting

**Problem**: Container won't start

```bash
docker logs optibot-api
# Check GEMINI_API_KEY is set
```

**Problem**: Terraform fails

```bash
az login
az account set --subscription "YOUR_SUB_ID"
```

**Problem**: Can't access Swagger

- Check VM firewall allows port 8000
- Check container is running: `docker ps`
