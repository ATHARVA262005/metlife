# 🚀 START HERE - Azure Portal Deployment

**Quick 3-step guide to deploy your API using Azure Portal (no CLI needed!)**

---

## 📖 Choose Your Guide

### 🎯 **RECOMMENDED: [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)**
**A simple checklist - perfect for following along step-by-step!**

### 📚 **DETAILED: [AZURE_PORTAL_GUIDE.md](AZURE_PORTAL_GUIDE.md)**
**Complete guide with explanations, troubleshooting, and tips**

---

## ⚡ Super Quick Start (10 minutes)

### Step 1: Push Docker Image (5 min)

Open PowerShell in this folder:

```powershell
# Login to Docker Hub (create free account at hub.docker.com)
docker login

# Build image (takes 3-5 minutes)
docker build -t claim-fraud-api:latest .

# Tag with YOUR Docker Hub username
docker tag claim-fraud-api:latest YOUR_USERNAME/claim-fraud-api:latest

# Push to Docker Hub
docker push YOUR_USERNAME/claim-fraud-api:latest
```

**✅ Your image:** `YOUR_USERNAME/claim-fraud-api:latest`

---

### Step 2: Create in Azure Portal (5 min)

1. Go to **[portal.azure.com](https://portal.azure.com)**
2. **Create a resource** → Search **"Container Instances"** → **Create**

**Fill in:**
- Resource group: `metlife-rg` (create new)
- Container name: `claim-fraud-api`
- Region: `East US`
- Image: `YOUR_USERNAME/claim-fraud-api:latest`
- Size: 1 CPU, 1.5 GB RAM
- Networking: Public, DNS name: `metlife-fraud-api`, Port: `8000`
- Environment variables:
  - `PORT` = `8000`
  - `GEMINI_API_KEY` = `AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0`

3. **Create** → Wait 2-3 minutes

---

### Step 3: Test Your API (1 min)

Your API URL will be:
```
http://metlife-fraud-api.eastus.azurecontainer.io:8000
```

**Open in browser:**
```
http://your-url:8000/docs
```

✅ **You'll see the Swagger UI with all 3 endpoints!**

---

## 📁 What's In This Repo

| File | Purpose |
|------|---------|
| **DEPLOY_CHECKLIST.md** | Simple checklist to follow |
| **AZURE_PORTAL_GUIDE.md** | Complete guide with screenshots descriptions |
| **Dockerfile** | Docker configuration (already done!) |
| **docker-compose.yml** | For local testing |
| **main.py** | Your FastAPI application |
| **ocr_processor.py** | OCR + AI fraud detection |
| **requirements.txt** | Python dependencies |

---

## 🧪 Test Locally First (Optional)

Before deploying to Azure, test locally:

```powershell
# Quick start script
.\docker-quick-start.ps1

# Or manually
docker build -t claim-fraud-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key claim-fraud-api

# Visit: http://localhost:8000/docs
```

---

## 💡 Key Points

✅ **No Azure CLI needed** - Everything done in browser!  
✅ **Free $200 credit** - New Azure accounts get this  
✅ **Tesseract OCR included** - Works out of the box  
✅ **Takes 10 minutes** - From Docker Hub to live API  
✅ **Stop to save money** - Only pay when running  

---

## 🎯 Your 3 API Endpoints

Once deployed, you'll have:

1. **POST /validate-zip-claim/**
   - Upload ZIP file with 10 JSON files
   - Returns fraud analysis

2. **GET /validate-local-folder/**
   - Test with server-side folders
   - Good for debugging

3. **POST /detect-fraud-from-pdf/**
   - Upload PDF with claim documents
   - OCR + AI fraud detection
   - Returns fraud score + analysis

---

## 💰 Cost Estimate

**Azure Container Instances:**
- **1 CPU, 1.5 GB RAM**: ~$34/month (24/7)
- **Your $200 credit**: Lasts ~6 months
- **Stop when not using**: Save money!

**Docker Hub:**
- **Free forever** for public images

---

## 🆘 Need Help?

1. **Check [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)** - Step-by-step guide
2. **Read [AZURE_PORTAL_GUIDE.md](AZURE_PORTAL_GUIDE.md)** - Detailed explanations
3. **Troubleshooting section** in both guides
4. **Check Azure Portal logs** - See what's happening

---

## 🎉 Quick Win

**Want to see it work right now?**

1. Already have Docker Hub account? ✅
2. Already built image? ✅
3. Go to Azure Portal now! 👉 [portal.azure.com](https://portal.azure.com)
4. Follow [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)
5. **Live in 10 minutes!** 🚀

---

## 📞 Documentation Links

- **Azure Portal**: https://portal.azure.com
- **Docker Hub**: https://hub.docker.com
- **Azure Free Account**: https://azure.microsoft.com/free/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

## ✨ What Makes This Special

✅ **Complete OCR solution** - Tesseract fully installed  
✅ **AI-powered** - Google Gemini integration  
✅ **Production-ready** - Proper error handling  
✅ **Secure** - Non-root user, environment variables  
✅ **Well-documented** - Multiple guides included  
✅ **Easy to deploy** - No command line if you prefer portal  

---

## 🗺️ Deployment Roadmap

```
1. Build Docker Image (5 min)
   └─> docker build, docker push
   
2. Deploy to Azure Portal (5 min)
   └─> Create Container Instance
   
3. Test API (1 min)
   └─> Open /docs, try endpoints
   
4. Show to judges (∞)
   └─> Win hackathon! 🏆
```

---

## 🔥 Ready to Deploy?

### Next Step: Open [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)

**Or jump straight in:**
1. `docker login`
2. `docker build -t claim-fraud-api .`
3. `docker tag claim-fraud-api YOUR_USERNAME/claim-fraud-api`
4. `docker push YOUR_USERNAME/claim-fraud-api`
5. Go to Azure Portal → Create Container Instance

**That's it! Good luck! 🍀**

---

## 🗑️ After Hackathon

**To stop charges:**
1. Azure Portal → Resource groups
2. Click `metlife-rg`
3. Delete resource group
4. Confirm

**Your code stays on GitHub forever!** ✅
**Your Docker image stays on Docker Hub!** ✅

---

**Questions? Check the detailed guides! 📚**

**Ready? Start with [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)! 🚀**
