# Deploying to Azure with Docker

This guide explains how to deploy your Claim Fraud Detection API to Azure using Docker containers.

## Prerequisites

1. **Azure Account**: [Sign up for free](https://azure.microsoft.com/free/) ($200 free credit)
2. **Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop)
3. **Azure CLI**: [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
4. **Your GitHub repository**: Already done! ✅

## Deployment Options

### Option 1: Azure Container Instances (ACI) - Simplest
- **Best for**: Testing, low traffic APIs
- **Cost**: ~$0.013/hour (~$10/month for 24/7)
- **Setup time**: 5 minutes
- **Pros**: Fastest deployment, pay-per-second billing
- **Cons**: No auto-scaling, cold starts

### Option 2: Azure App Service (Container) - Recommended
- **Best for**: Production APIs, auto-scaling
- **Cost**: Free tier available, Basic starts at $13/month
- **Setup time**: 10 minutes
- **Pros**: Auto-scaling, custom domains, SSL, CI/CD
- **Cons**: Slightly more expensive

### Option 3: Azure Container Apps - Modern
- **Best for**: Microservices, serverless containers
- **Cost**: Pay-per-use, generous free tier
- **Setup time**: 10 minutes
- **Pros**: Auto-scaling to zero, event-driven
- **Cons**: Newer service, less documentation

---

## Option 1: Deploy to Azure Container Instances (Fastest)

### Step 1: Install Azure CLI and Docker
```bash
# Verify installations
az --version
docker --version
```

### Step 2: Build and Test Docker Image Locally
```bash
# Build the Docker image
docker build -t claim-fraud-api:latest .

# Test locally (optional)
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key_here claim-fraud-api:latest

# Visit http://localhost:8000/docs to test
```

### Step 3: Login to Azure
```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Step 4: Create Azure Resources
```bash
# Create a resource group
az group create --name metlife-rg --location eastus

# Create Azure Container Registry (ACR)
az acr create --resource-group metlife-rg \
  --name metliferegistry \
  --sku Basic \
  --location eastus

# Enable admin access (needed for ACI)
az acr update --name metliferegistry --admin-enabled true
```

### Step 5: Push Docker Image to Azure Container Registry
```bash
# Login to ACR
az acr login --name metliferegistry

# Tag your image
docker tag claim-fraud-api:latest metliferegistry.azurecr.io/claim-fraud-api:latest

# Push to ACR
docker push metliferegistry.azurecr.io/claim-fraud-api:latest
```

### Step 6: Deploy to Azure Container Instances
```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name metliferegistry --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name metliferegistry --query "passwords[0].value" -o tsv)

# Deploy container
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
  --cpu 1 \
  --memory 1.5 \
  --location eastus
```

### Step 7: Get Your API URL
```bash
# Get the FQDN (Fully Qualified Domain Name)
az container show \
  --resource-group metlife-rg \
  --name claim-fraud-api \
  --query ipAddress.fqdn \
  --output tsv
```

Your API will be available at: `http://metlife-fraud-api.eastus.azurecontainer.io:8000`

### Step 8: Test Your Deployed API
```bash
# Test root endpoint
curl http://metlife-fraud-api.eastus.azurecontainer.io:8000/

# Open API docs in browser
# Visit: http://metlife-fraud-api.eastus.azurecontainer.io:8000/docs
```

---

## Option 2: Deploy to Azure App Service (Recommended for Production)

### Step 1-5: Same as Option 1 (Build and push to ACR)

### Step 6: Create App Service Plan
```bash
# Create App Service Plan (Linux with container support)
az appservice plan create \
  --name metlife-plan \
  --resource-group metlife-rg \
  --is-linux \
  --sku B1 \
  --location eastus
```

### Step 7: Create Web App from Container
```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name metliferegistry --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name metliferegistry --query "passwords[0].value" -o tsv)

# Create web app
az webapp create \
  --resource-group metlife-rg \
  --plan metlife-plan \
  --name metlife-fraud-api \
  --deployment-container-image-name metliferegistry.azurecr.io/claim-fraud-api:latest

# Configure registry credentials
az webapp config container set \
  --name metlife-fraud-api \
  --resource-group metlife-rg \
  --docker-custom-image-name metliferegistry.azurecr.io/claim-fraud-api:latest \
  --docker-registry-server-url https://metliferegistry.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Set environment variables
az webapp config appsettings set \
  --resource-group metlife-rg \
  --name metlife-fraud-api \
  --settings GEMINI_API_KEY=AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0 PORT=8000
```

### Step 8: Enable Continuous Deployment (Optional)
```bash
# Configure webhook for auto-deploy on new images
az webapp deployment container config \
  --name metlife-fraud-api \
  --resource-group metlife-rg \
  --enable-cd true
```

Your API will be at: `https://metlife-fraud-api.azurewebsites.net`

---

## Option 3: Deploy Using Azure Portal (No CLI)

### Step 1: Build and Tag Docker Image
```bash
docker build -t claim-fraud-api:latest .
```

### Step 2: Push to Docker Hub (Alternative to ACR)
```bash
# Login to Docker Hub
docker login

# Tag image with your Docker Hub username
docker tag claim-fraud-api:latest YOUR_DOCKERHUB_USERNAME/claim-fraud-api:latest

# Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/claim-fraud-api:latest
```

### Step 3: Deploy via Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Containers" → "Container Instances"
3. Fill in:
   - **Basics**:
     - Resource group: Create new "metlife-rg"
     - Container name: claim-fraud-api
     - Region: East US
     - Image source: Docker Hub or other registry
     - Image: YOUR_DOCKERHUB_USERNAME/claim-fraud-api:latest
   - **Networking**:
     - Networking type: Public
     - DNS name label: metlife-fraud-api
     - Ports: 8000 (TCP)
   - **Advanced**:
     - Environment variables:
       - `PORT` = `8000`
       - `GEMINI_API_KEY` = `your_api_key`
     - CPU: 1 core
     - Memory: 1.5 GB
4. Click "Review + create" → "Create"

---

## Environment Variables Setup

### Required Environment Variables:
```bash
PORT=8000
GEMINI_API_KEY=AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0
```

### Set via Azure CLI:
```bash
# For Container Instances
az container create ... --environment-variables PORT=8000 GEMINI_API_KEY=your_key

# For App Service
az webapp config appsettings set \
  --name metlife-fraud-api \
  --resource-group metlife-rg \
  --settings PORT=8000 GEMINI_API_KEY=your_key
```

---

## Testing Your Deployed API

### 1. Health Check
```bash
curl https://metlife-fraud-api.azurewebsites.net/
```

### 2. Interactive Docs
Open in browser:
```
https://metlife-fraud-api.azurewebsites.net/docs
```

### 3. Test ZIP Validation
```bash
curl -X POST "https://metlife-fraud-api.azurewebsites.net/validate-zip-claim/" \
  -H "accept: application/json" \
  -F "file=@claim_folder_001.zip"
```

### 4. Test PDF Fraud Detection
```bash
curl -X POST "https://metlife-fraud-api.azurewebsites.net/detect-fraud-from-pdf/?gemini_api_key=YOUR_KEY" \
  -H "accept: application/json" \
  -F "pdf_file=@claim_document.pdf"
```

---

## Continuous Deployment (CI/CD)

### GitHub Actions Workflow (Automatic Deployment)

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Build and push Docker image
      run: |
        az acr login --name metliferegistry
        docker build -t metliferegistry.azurecr.io/claim-fraud-api:${{ github.sha }} .
        docker tag metliferegistry.azurecr.io/claim-fraud-api:${{ github.sha }} metliferegistry.azurecr.io/claim-fraud-api:latest
        docker push metliferegistry.azurecr.io/claim-fraud-api:${{ github.sha }}
        docker push metliferegistry.azurecr.io/claim-fraud-api:latest
    
    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: metlife-fraud-api
        images: metliferegistry.azurecr.io/claim-fraud-api:${{ github.sha }}
```

### Setup GitHub Secrets:
1. Generate Azure credentials:
```bash
az ad sp create-for-rbac --name "github-actions" --sdk-auth --role contributor \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/metlife-rg
```

2. Copy the JSON output
3. In GitHub repo → Settings → Secrets → New secret
4. Name: `AZURE_CREDENTIALS`
5. Value: Paste the JSON

Now every push to `main` will auto-deploy!

---

## Monitoring and Logs

### View Logs (Container Instances)
```bash
az container logs --resource-group metlife-rg --name claim-fraud-api --follow
```

### View Logs (App Service)
```bash
az webapp log tail --name metlife-fraud-api --resource-group metlife-rg
```

### Azure Portal Monitoring
1. Go to your resource in Azure Portal
2. Click "Monitoring" → "Logs"
3. View metrics: CPU, Memory, Request count, Response time

---

## Scaling

### Container Instances (Manual Scaling)
```bash
# Update CPU/Memory
az container create ... --cpu 2 --memory 3.5
```

### App Service (Auto-scaling)
```bash
# Enable auto-scaling
az monitor autoscale create \
  --resource-group metlife-rg \
  --resource metlife-fraud-api \
  --resource-type Microsoft.Web/sites \
  --name autoscale-plan \
  --min-count 1 \
  --max-count 5 \
  --count 2

# Scale based on CPU
az monitor autoscale rule create \
  --resource-group metlife-rg \
  --autoscale-name autoscale-plan \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

---

## Cost Optimization

### Free/Cheap Options:
1. **Azure Container Instances**: Stop when not in use
```bash
az container stop --resource-group metlife-rg --name claim-fraud-api
az container start --resource-group metlife-rg --name claim-fraud-api
```

2. **App Service Free Tier**: Limited to 60 min/day CPU time
```bash
az appservice plan create --name metlife-plan --resource-group metlife-rg --sku F1 --is-linux
```

3. **Azure Container Apps**: Auto-scale to zero (pay only when used)

### Monthly Cost Estimates:
- **Container Instances (B1)**: ~$10/month (1 CPU, 1.5GB RAM, 24/7)
- **App Service (B1)**: ~$13/month (1 CPU, 1.75GB RAM, 24/7)
- **App Service (F1)**: FREE (60 min/day, 1GB RAM)
- **Container Apps**: ~$5-20/month (depends on usage)

---

## Troubleshooting

### Container won't start
```bash
# Check container logs
az container logs --resource-group metlife-rg --name claim-fraud-api

# Common issues:
# 1. Port mismatch: Ensure PORT=8000 is set
# 2. Missing dependencies: Check Dockerfile
# 3. Tesseract not found: Verify apt-get install worked
```

### API returns 502/503
```bash
# Check if app is running
az container show --resource-group metlife-rg --name claim-fraud-api

# Restart container
az container restart --resource-group metlife-rg --name claim-fraud-api
```

### OCR endpoint fails
```bash
# Verify Tesseract is installed in container
az container exec \
  --resource-group metlife-rg \
  --name claim-fraud-api \
  --exec-command "tesseract --version"
```

---

## Security Best Practices

### 1. Use Azure Key Vault for Secrets
```bash
# Create Key Vault
az keyvault create --name metlife-vault --resource-group metlife-rg --location eastus

# Store API key
az keyvault secret set --vault-name metlife-vault --name gemini-api-key --value YOUR_KEY

# Grant access to App Service
az webapp identity assign --resource-group metlife-rg --name metlife-fraud-api
az keyvault set-policy --name metlife-vault --object-id IDENTITY_ID --secret-permissions get
```

### 2. Enable HTTPS Only (App Service)
```bash
az webapp update --resource-group metlife-rg --name metlife-fraud-api --https-only true
```

### 3. Configure CORS (if needed)
```bash
az webapp cors add --resource-group metlife-rg --name metlife-fraud-api --allowed-origins "*"
```

---

## Cleanup (Delete Resources)

### Delete Everything
```bash
# Delete entire resource group (removes all resources)
az group delete --name metlife-rg --yes --no-wait
```

### Delete Individual Resources
```bash
# Delete container
az container delete --resource-group metlife-rg --name claim-fraud-api --yes

# Delete app service
az webapp delete --resource-group metlife-rg --name metlife-fraud-api

# Delete container registry
az acr delete --resource-group metlife-rg --name metliferegistry --yes
```

---

## Quick Start Commands Summary

```bash
# 1. Build Docker image
docker build -t claim-fraud-api:latest .

# 2. Login to Azure
az login

# 3. Create resource group
az group create --name metlife-rg --location eastus

# 4. Create and configure ACR
az acr create --name metliferegistry --resource-group metlife-rg --sku Basic
az acr update --name metliferegistry --admin-enabled true
az acr login --name metliferegistry

# 5. Push image
docker tag claim-fraud-api:latest metliferegistry.azurecr.io/claim-fraud-api:latest
docker push metliferegistry.azurecr.io/claim-fraud-api:latest

# 6. Deploy to ACI
az container create \
  --resource-group metlife-rg \
  --name claim-fraud-api \
  --image metliferegistry.azurecr.io/claim-fraud-api:latest \
  --dns-name-label metlife-fraud-api \
  --ports 8000 \
  --environment-variables PORT=8000 GEMINI_API_KEY=your_key \
  --cpu 1 --memory 1.5

# 7. Get URL
az container show --resource-group metlife-rg --name claim-fraud-api --query ipAddress.fqdn -o tsv
```

---

## Support Resources

- **Azure Documentation**: https://docs.microsoft.com/azure
- **Azure Container Instances**: https://docs.microsoft.com/azure/container-instances/
- **Azure App Service**: https://docs.microsoft.com/azure/app-service/
- **Docker Documentation**: https://docs.docker.com/
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

## Next Steps

1. ✅ Build Docker image locally
2. ✅ Test locally with `docker run`
3. ✅ Push to Azure Container Registry
4. ✅ Deploy to Azure Container Instances or App Service
5. ✅ Test deployed API
6. ✅ Set up monitoring
7. ✅ Configure CI/CD (optional)
8. ✅ Add custom domain (optional)

**Your API will be live at**: `http://metlife-fraud-api.eastus.azurecontainer.io:8000` or `https://metlife-fraud-api.azurewebsites.net`

**API Documentation**: Add `/docs` to your URL to access Swagger UI

Good luck with your hackathon! 🚀
