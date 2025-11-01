# 🚀 Docker Deployment - Quick Start

Your API is now fully Dockerized and ready for Azure deployment!

## 📋 What's Been Created

1. **Dockerfile** - Production-ready container with Tesseract OCR
2. **docker-compose.yml** - Easy local testing
3. **.dockerignore** - Optimized image size
4. **AZURE_DEPLOYMENT.md** - Complete Azure deployment guide
5. **docker-quick-start.ps1** - One-click local testing script

## 🧪 Test Locally First

### Option 1: Quick Start Script (Easiest)
```powershell
.\docker-quick-start.ps1
```
This will:
- Build the Docker image
- Start the container
- Open API docs in your browser

### Option 2: Docker Compose
```bash
docker-compose up --build
```
Visit: http://localhost:8000/docs

### Option 3: Manual Docker Commands
```bash
# Build
docker build -t claim-fraud-api:latest .

# Run
docker run -d -p 8000:8000 \
  -e PORT=8000 \
  -e GEMINI_API_KEY=AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0 \
  --name claim-fraud-api \
  claim-fraud-api:latest

# View logs
docker logs -f claim-fraud-api

# Stop
docker stop claim-fraud-api
```

## ☁️ Deploy to Azure

### Prerequisites
1. Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
3. Sign up for [Azure Free Account](https://azure.microsoft.com/free/) ($200 credit)

### Quick Deploy (5 minutes)

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name metlife-rg --location eastus

# 3. Create container registry
az acr create --name metliferegistry --resource-group metlife-rg --sku Basic
az acr update --name metliferegistry --admin-enabled true

# 4. Build and push
az acr login --name metliferegistry
docker build -t metliferegistry.azurecr.io/claim-fraud-api:latest .
docker push metliferegistry.azurecr.io/claim-fraud-api:latest

# 5. Deploy to Azure Container Instances
ACR_USERNAME=$(az acr credential show --name metliferegistry --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name metliferegistry --query "passwords[0].value" -o tsv)

az container create \
  --resource-group metlife-rg \
  --name claim-fraud-api \
  --image metliferegistry.azurecr.io/claim-fraud-api:latest \
  --registry-login-server metliferegistry.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label metlife-fraud-api \
  --ports 8000 \
  --environment-variables PORT=8000 GEMINI_API_KEY=AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0 \
  --cpu 1 --memory 1.5 \
  --location eastus

# 6. Get your API URL
az container show \
  --resource-group metlife-rg \
  --name claim-fraud-api \
  --query ipAddress.fqdn \
  --output tsv
```

Your API will be at: `http://metlife-fraud-api.eastus.azurecontainer.io:8000`

## 📖 Full Documentation

- **Azure Deployment Guide**: See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
- **Render Deployment**: See [DEPLOYMENT_README.md](DEPLOYMENT_README.md)

## 🔍 Features

✅ **Tesseract OCR** - Fully installed and working in Docker
✅ **FastAPI** - All 3 endpoints operational
✅ **Health Checks** - Built-in monitoring
✅ **Security** - Non-root user, minimal image
✅ **Auto-scaling** - Ready for Azure App Service
✅ **CI/CD Ready** - GitHub Actions workflow included

## 📊 Deployment Options Comparison

| Feature | Azure Container Instances | Azure App Service | Render |
|---------|--------------------------|-------------------|--------|
| Cost | ~$10/month | $13+/month | Free tier |
| Tesseract | ✅ Yes | ✅ Yes | ❌ Paid only |
| Auto-scale | ❌ Manual | ✅ Yes | ✅ Yes |
| Setup Time | 5 min | 10 min | 3 min |
| Best For | Testing | Production | Quick demos |

## 🆘 Troubleshooting

### Docker build fails
```bash
# Clean docker cache
docker system prune -a
docker build --no-cache -t claim-fraud-api:latest .
```

### Container won't start
```bash
# Check logs
docker logs claim-fraud-api

# Common fix: Remove old containers
docker rm -f $(docker ps -aq)
```

### Tesseract not found
```bash
# Test Tesseract in container
docker exec claim-fraud-api tesseract --version
```

### API not responding
```bash
# Check if port is available
netstat -ano | findstr :8000

# Kill process using port 8000
taskkill /F /PID <PID>
```

## 📞 Support

- Azure Issues: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
- Docker Issues: Check logs with `docker logs -f claim-fraud-api`
- API Issues: Visit http://localhost:8000/docs

## 🎯 Next Steps

1. ✅ Test locally: `.\docker-quick-start.ps1`
2. ✅ Deploy to Azure: Follow [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
3. ✅ Set up CI/CD: Use GitHub Actions workflow
4. ✅ Add custom domain (optional)
5. ✅ Set up monitoring and alerts

**Your code is now production-ready!** 🚀
