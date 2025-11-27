# Optibot Assistant

AI-powered chatbot assistant using RAG (Retrieval-Augmented Generation) with Gemini embeddings and ChromaDB vector store. Includes automated daily scraper with delta detection.

## 🚀 Features

- **FastAPI REST API** with Swagger UI documentation
- **RAG-based Q&A** using Gemini embeddings + ChromaDB
- **Daily scraper job** with delta detection (hash-based)
- **Automated CI/CD** with GitHub Actions + GHCR
- **Infrastructure as Code** with Terraform (Azure VM)
- **Docker containerized** deployment

## 📋 Prerequisites

- Python 3.10+
- Docker
- Gemini API Key ([Get one here](https://ai.google.dev/))
- Azure account (for deployment)
- Terraform (for infrastructure)

## 🛠️ Local Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/mahara0511/nguyenminhkhanhtest.git
cd nguyenminhkhanhtest

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.sample .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run Locally

**Option A: Python directly**

```bash
# Run API
uvicorn assistant.run:app --host 0.0.0.0 --port 8000

# Run scraper (one-time)
python -m scraper.daily_job
```

**Option B: Docker**

```bash
# Build image
docker build -t optibot-assistant .

# Run API
docker run --rm -p 8000:8000 \
  -e GEMINI_API_KEY="your_key" \
  -v $(pwd)/chroma_storage:/app/chroma_storage \
  optibot-assistant

# Run scraper
docker run --rm \
  -e GEMINI_API_KEY="your_key" \
  -v $(pwd)/chroma_storage:/app/chroma_storage \
  optibot-assistant \
  python -m scraper.daily_job
```

### 4. Access the API

- **API endpoint**: http://localhost:8000/ask
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🌐 Deployment (Azure VM with Terraform)

### 1. Setup Azure CLI

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### 2. Configure Terraform Variables

Create `infra/terraform.tfvars`:

```hcl
gemini_api_key   = "your_gemini_api_key"
github_token     = "your_github_pat"
github_username  = "mahara0511"
docker_image     = "ghcr.io/mahara0511/nguyenminhkhanhtest:latest"
```

### 3. Deploy Infrastructure

```bash
cd infra

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply (create VM)
terraform apply
```

After deployment, Terraform will output:

- Public IP address
- SSH command
- API URL
- Swagger URL

### 4. Setup GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

- `AZURE_VM_HOST`: VM public IP from Terraform output
- `AZURE_VM_USER`: `azureuser` (default)
- `AZURE_VM_SSH_KEY`: Your SSH private key
- `GEMINI_API_KEY`: Your Gemini API key

### 5. Deploy via CI/CD

```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

GitHub Actions will automatically:

1. Build Docker image
2. Push to GitHub Container Registry
3. SSH to VM and deploy

## 📊 Daily Scraper Job

The scraper runs automatically at **2:00 AM daily** on the VM.

### What it does:

1. Re-scrapes all articles from Optisigns support API
2. Computes SHA256 hash of each article's markdown content
3. Detects changes:
   - **Added**: New articles not in previous state
   - **Updated**: Existing articles with changed content
   - **Skipped**: Unchanged articles
4. Uploads only **added/updated** articles to ChromaDB
5. Logs results to `/var/log/optibot/scraper.log`

### View logs:

**On VM:**

```bash
ssh azureuser@YOUR_VM_IP
tail -f /var/log/optibot/scraper.log
```

**Latest run summary:**

```bash
cat /var/log/optibot/scraper.log | grep "DAILY JOB RESULT" -A 3
```

Example output:

```
=== DAILY JOB RESULT ===
Added:    5
Updated:  2
Skipped:  143
```

## 🧪 Testing the API

### Using curl:

```bash
curl -X POST http://YOUR_VM_IP:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Optisigns free plan?"}'
```

### Using Swagger UI:

1. Open http://YOUR_VM_IP:8000/docs
2. Click "POST /ask" → "Try it out"
3. Enter question in JSON body
4. Click "Execute"

## 📂 Project Structure

```
.
├── assistant/          # RAG assistant (FastAPI app)
│   ├── graph.py       # LangGraph workflow
│   ├── run.py         # FastAPI app + CLI
│   └── nodes/         # Graph nodes (embed, search, etc.)
├── scraper/           # Web scraper
│   ├── graph.py       # Scraper LangGraph
│   ├── daily_job.py   # Daily job with delta detection
│   └── nodes/         # Scraper nodes
├── loader/            # Vector store utilities
│   └── vector_store.py
├── infra/             # Terraform infrastructure
│   ├── main.tf
│   ├── variables.tf
│   └── cloud-init.yml
├── .github/workflows/ # CI/CD pipelines
├── Dockerfile         # Container definition
└── requirements.txt   # Python dependencies
```

## 🔐 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Use GitHub Secrets for sensitive data in CI/CD
- Rotate API keys regularly
- Consider using Azure Key Vault for production

## 📝 License

MIT

## 👤 Author

mahara0511
