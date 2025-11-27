# Deployment Summary

## ✅ What Has Been Set Up

### 1. Docker Configuration

- **Dockerfile**: Configured to run FastAPI assistant API on port 8000
- **Image includes**: Python 3.10, all dependencies, ChromaDB, Gemini SDK
- **Swagger UI**: Auto-enabled at `/docs` endpoint

### 2. Application Structure

- **Assistant API** (`assistant/run.py`):
  - FastAPI app with `/ask` endpoint
  - Swagger documentation at `/docs`
  - Logs startup with Swagger URL
- **Daily Scraper** (`scraper/daily_job.py`):

  - Re-scrapes Optisigns support articles
  - Hash-based delta detection (SHA256)
  - Logs: Added, Updated, Skipped counts
  - Only uploads changes to ChromaDB

- **Utilities** (`scraper/utils.py`):
  - `load_hash_db()` / `save_hash_db()`
  - Persists state in `scraper_hash.json`

### 3. CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers**: Push to `main` branch

**Build Job**:

- Builds Docker image
- Pushes to GitHub Container Registry (ghcr.io)
- Tags with commit SHA and `:latest`

**Deploy Job**:

- SSHs to Azure VM
- Pulls latest image
- Stops old container
- Starts new container with environment variables
- Automatically restarts on failure

**Required GitHub Secrets**:

- `AZURE_VM_HOST`: VM public IP
- `AZURE_VM_USER`: `azureuser`
- `AZURE_VM_SSH_KEY`: SSH private key
- `GEMINI_API_KEY`: Gemini API key

### 4. Terraform Infrastructure (`infra/`)

**Resources Created**:

- Resource Group
- Virtual Network + Subnet
- Public IP (static)
- Network Security Group (ports 22, 8000)
- Network Interface
- Ubuntu 22.04 VM (Standard_B2s)

**Cloud-Init Automation**:

- Installs Docker
- Creates `/opt/optibot/` directory structure
- Logs into GHCR
- Pulls Docker image
- Runs API container
- Sets up cron job (2 AM daily)

**Outputs**:

- Public IP address
- SSH command
- API URL
- Swagger URL

### 5. Configuration Files

- `.env.sample`: Template for local development
- `terraform.tfvars.example`: Template for Terraform variables
- `.gitignore`: Updated to exclude secrets, state files, DB

### 6. Documentation

- **README.md**: Full documentation
- **QUICKSTART.md**: 5-minute getting started guide
- **deploy.sh**: Automated deployment script

## 🚀 Deployment Steps

### Option A: Automated (Recommended)

```bash
# 1. Configure
cd infra
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 2. Deploy
cd ..
./deploy.sh
```

### Option B: Manual

```bash
# 1. Build and push image
docker build -t optibot-assistant .
docker tag optibot-assistant ghcr.io/mahara0511/nguyenminhkhanhtest:latest
echo YOUR_GH_TOKEN | docker login ghcr.io -u mahara0511 --password-stdin
docker push ghcr.io/mahara0511/nguyenminhkhanhtest:latest

# 2. Deploy infrastructure
cd infra
terraform init
terraform apply

# 3. Get VM IP
terraform output public_ip_address

# 4. Setup GitHub Secrets for CI/CD
# (Manual step in GitHub UI)
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│  ┌──────────────┐         ┌─────────────────────────┐  │
│  │ Source Code  │────────▶│  GitHub Actions CI/CD   │  │
│  └──────────────┘         └──────────┬──────────────┘  │
│         │                             │                  │
└─────────┼─────────────────────────────┼──────────────────┘
          │                             │
          │                             ▼
          │                  ┌────────────────────────┐
          │                  │ GitHub Container       │
          │                  │ Registry (GHCR)        │
          │                  └──────────┬─────────────┘
          │                             │
          ▼                             ▼
┌─────────────────────────────────────────────────────────┐
│                     Azure VM (Ubuntu)                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Docker Container: optibot-api                   │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  FastAPI App (port 8000)                   │  │  │
│  │  │  - /ask endpoint                           │  │  │
│  │  │  - /docs (Swagger)                         │  │  │
│  │  │  - ChromaDB (vector store)                 │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Cron Job (2 AM daily)                          │  │
│  │  - Run scraper container                        │  │
│  │  - Detect added/updated/skipped                 │  │
│  │  - Update ChromaDB                              │  │
│  │  - Log to /var/log/optibot/scraper.log         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  📁 /opt/optibot/chroma_storage (persistent volume)     │
└─────────────────────────────────────────────────────────┘
```

## 🔍 Verification Checklist

After deployment, verify:

- [ ] VM is accessible via SSH
- [ ] API responds at `http://VM_IP:8000/ask`
- [ ] Swagger UI loads at `http://VM_IP:8000/docs`
- [ ] Container is running: `docker ps | grep optibot-api`
- [ ] Cron job is configured: `crontab -l`
- [ ] Log directory exists: `ls /var/log/optibot/`
- [ ] ChromaDB directory: `ls /opt/optibot/chroma_storage/`

## 🔐 Security Reminders

- ✅ `.env` is in `.gitignore`
- ✅ Terraform state files excluded
- ✅ API keys stored in GitHub Secrets
- ✅ SSH key authentication only
- ⚠️ Port 8000 is public (consider adding authentication)
- ⚠️ Consider using Azure Key Vault for production

## 📝 Next Steps

1. **Test locally** first with Docker
2. **Deploy infrastructure** with Terraform
3. **Configure GitHub Secrets** for CI/CD
4. **Push to main** branch to trigger deployment
5. **Monitor logs** to verify scraper runs
6. **Test API** with sample questions

## 🆘 Support

See documentation:

- Full guide: [README.md](README.md)
- Quick start: [QUICKSTART.md](QUICKSTART.md)
- Terraform: [infra/](infra/)
- CI/CD: [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
