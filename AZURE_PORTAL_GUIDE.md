# 🚀 Deploy to Azure Using Portal (No CLI Required!)

**Complete visual guide for deploying your Dockerized API to Azure using only the web browser.**

---

## 📋 Prerequisites

1. ✅ **Azure Account** - [Sign up free here](https://azure.microsoft.com/free/) ($200 free credit!)
2. ✅ **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop) (to build image)
3. ✅ **Docker Hub Account** - [Sign up free](https://hub.docker.com/signup) (to host your image)

---

## 🎯 Quick Overview

We'll do 3 simple steps:
1. **Build & Push** your Docker image to Docker Hub (5 min)
2. **Create Container** in Azure Portal (5 min)
3. **Test your API** (1 min)

**Total Time: ~10 minutes**

---

## Part 1: Build and Push Docker Image (One-time setup)

### Step 1.1: Open PowerShell/Terminal in your project folder

```powershell
cd D:\hackathon\metlife\3
```

### Step 1.2: Login to Docker Hub

```powershell
docker login
```
- Enter your Docker Hub username
- Enter your Docker Hub password

### Step 1.3: Build your Docker image

```powershell
docker build -t claim-fraud-api:latest .
```
⏱️ *Takes 3-5 minutes (downloads Python, installs Tesseract OCR, etc.)*

### Step 1.4: Tag the image with your Docker Hub username

```powershell
# YOUR username (already done!)
docker tag claim-fraud-api:latest atharvaralegankar/claim-fraud-api:latest
```

### Step 1.5: Push to Docker Hub

```powershell
# YOUR image (already pushed!)
docker push atharvaralegankar/claim-fraud-api:latest
```

✅ **Already completed! Your image is live!**

⏱️ *Takes 2-3 minutes*

✅ **Your Docker image is now public at:** `YOUR_USERNAME/claim-fraud-api:latest`

---

## Part 2: Deploy on Azure Portal

### Step 2.1: Open Azure Portal

1. Go to **[portal.azure.com](https://portal.azure.com)**
2. Sign in with your Microsoft account

### Step 2.2: Create a Container Instance

1. Click **"Create a resource"** (top left or center of home page)
2. Search for **"Container Instances"**
3. Click **"Container Instances"** from results
4. Click **"Create"**

### Step 2.3: Fill in BASICS Tab

**Project Details:**
- **Subscription**: Select your subscription (e.g., "Free Trial" or "Pay-As-You-Go")
- **Resource group**: Click "Create new" → Enter: `metlife-rg` → Click OK

**Container Details:**
- **Container name**: `claim-fraud-api`
- **Region**: Choose closest to you (e.g., `(US) East US`)
- **Availability zones**: Leave default
- **SKU**: `Standard`

**Image source:**
- **Image source**: Select **"Other registry"**
- **Image type**: `Public`
- **Image**: `atharvaralegankar/claim-fraud-api:latest`
  
  ⭐ **Use exactly this:** `atharvaralegankar/claim-fraud-api:latest`

**Size:**
- **OS type**: `Linux`
- **Size**: Click "Change size"
  - CPU: `1` core
  - Memory: `1.5` GiB
  - Click "OK"

Click **"Next: Networking >"**

### Step 2.4: Fill in NETWORKING Tab

**Networking type:**
- Select **"Public"**

**DNS name label:**
- Enter: `metlife-fraud-api` (or any unique name)
- This will be your URL: `metlife-fraud-api.eastus.azurecontainer.io`

**DNS name label scope reuse:** (ignore this, leave default)

**Ports:**
- **Port**: `8000`
- **Protocol**: `TCP`

Click **"Next: Advanced >"**

### Step 2.5: Fill in ADVANCED Tab

**Restart policy:**
- Select: **"Always"** (so it auto-restarts if it crashes)

**Environment variables:**
Click **"+ Add"** to add each variable:

| Name | Value |
|------|-------|
| `PORT` | `8000` |
| `GEMINI_API_KEY` | `AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0` |

**Command override:** Leave empty

Click **"Next: Tags >"** (optional, skip if you want)

### Step 2.6: Review and Create

1. Click **"Next: Review + create >"**
2. Review your settings
3. Click **"Create"**

⏱️ **Deployment takes 2-3 minutes**

You'll see: "Deployment is in progress..."

---

## Part 3: Get Your API URL

### Once deployment completes:

1. Click **"Go to resource"**
2. On the Overview page, you'll see:
   - **Status**: Running ✅
   - **FQDN** (Fully Qualified Domain Name): This is your URL!

**Your API URL will be:**
```
http://metlife-fraud-api.eastus.azurecontainer.io:8000
```

*(The exact URL depends on your DNS name and region)*

---

## 🧪 Test Your Deployed API

### Option 1: Test in Browser

1. Copy your FQDN from Azure Portal
2. Add `/docs` to the end
3. Open in browser:
   ```
   http://metlife-fraud-api.eastus.azurecontainer.io:8000/docs
   ```

You'll see the interactive API documentation!

### Option 2: Test with PowerShell

```powershell
# Replace with your actual URL
$API_URL = "http://metlife-fraud-api.eastus.azurecontainer.io:8000"

# Test root endpoint
Invoke-WebRequest -Uri "$API_URL/" -UseBasicParsing

# Should return: "Claim Validation API is running"
```

### Option 3: Test Endpoints

**Test Root:**
```
http://your-url:8000/
```

**Test API Docs:**
```
http://your-url:8000/docs
```

**Test ZIP Upload** (use the Swagger UI at `/docs`)

---

## 📊 Monitor Your Container

### View Logs

1. In Azure Portal, go to your Container Instance
2. Click **"Containers"** in left menu
3. Click **"Logs"** tab
4. You'll see live logs from your FastAPI server

### Check Metrics

1. Click **"Metrics"** in left menu
2. Add metrics:
   - CPU Usage
   - Memory Usage
   - Network bytes

### Restart Container

1. Click **"Overview"**
2. Click **"Restart"** at the top
3. Confirm

### Stop Container (to save money)

1. Click **"Overview"**
2. Click **"Stop"** at the top
3. Start again when needed with **"Start"**

---

## 💰 Cost Information

### Azure Container Instances Pricing (East US):
- **Per second billing**
- **1 core, 1.5 GB**: ~$0.0000133/second
- **Running 24/7**: ~$34/month
- **Running 8 hours/day**: ~$11/month

### Free Credits:
- New Azure accounts get **$200 free credit** for 30 days
- That's enough for ~6 months of 24/7 running!

### Stop when not using:
```
Running time per month:
- 24/7: $34/month
- 12h/day: $17/month
- 8h/day: $11/month
- 4h/day: $5.5/month
```

**💡 Tip:** Stop your container when not demoing to save money!

---

## 🔧 Update Your API (After Code Changes)

### When you update your code:

1. **Rebuild and push Docker image:**
   ```powershell
   docker build -t YOUR_USERNAME/claim-fraud-api:latest .
   docker push YOUR_USERNAME/claim-fraud-api:latest
   ```

2. **Restart Azure Container:**
   - Go to Azure Portal → Your Container
   - Click "Restart"
   - Azure will pull the latest image from Docker Hub

That's it! ✅

---

## 🐛 Troubleshooting

### Problem: Container shows "Waiting" status

**Solution:**
- Wait 2-3 minutes for first-time deployment
- Check Docker Hub - is your image public?
- Check container logs for errors

### Problem: Can't access the URL

**Solution:**
- Make sure port is `8000`
- Make sure networking is "Public"
- Check if container status is "Running"
- Try without `https://` - use `http://`

### Problem: API returns errors

**Solution:**
- Check Logs in Azure Portal
- Verify environment variables are set:
  - `PORT=8000`
  - `GEMINI_API_KEY=your_key`
- Make sure image name is correct

### Problem: "Tesseract not found" error

**Solution:**
- This means Tesseract wasn't installed in Docker
- Rebuild your Docker image using our Dockerfile
- Make sure Dockerfile includes:
  ```dockerfile
  RUN apt-get update && apt-get install -y \
      tesseract-ocr \
      tesseract-ocr-eng
  ```

### Problem: Container keeps restarting

**Solution:**
- Check logs for Python errors
- Test Docker image locally first:
  ```powershell
  docker run -p 8000:8000 -e PORT=8000 YOUR_USERNAME/claim-fraud-api:latest
  ```
- If it works locally, the issue is with Azure settings

---

## 🔐 Security Best Practices

### 1. Hide your API Key

Instead of hardcoding in environment variables:
- Use Azure Key Vault (advanced)
- Or pass API key in request headers

### 2. Enable HTTPS

For production:
1. Use Azure Application Gateway
2. Or deploy to Azure App Service instead (has built-in SSL)

### 3. Restrict Access

Add authentication:
- Use Azure API Management
- Or add API keys in your FastAPI code

---

## 🎉 You're Done!

### What You've Deployed:

✅ **FastAPI** with 3 endpoints:
- `/validate-zip-claim/` - Upload ZIP files
- `/validate-local-folder/` - Test with server files
- `/detect-fraud-from-pdf/` - OCR + AI fraud detection

✅ **Tesseract OCR** - Fully working in container

✅ **Google Gemini AI** - Integrated for fraud detection

✅ **Public API** - Accessible from anywhere

### Your API URL:
```
http://metlife-fraud-api.eastus.azurecontainer.io:8000
```

### API Documentation:
```
http://metlife-fraud-api.eastus.azurecontainer.io:8000/docs
```

---

## 📱 Share Your API

Send this to teammates:
```
🚀 MetLife Fraud Detection API

API URL: http://metlife-fraud-api.eastus.azurecontainer.io:8000
Docs: http://metlife-fraud-api.eastus.azurecontainer.io:8000/docs

Endpoints:
- POST /validate-zip-claim/ - Upload claim ZIP
- GET /validate-local-folder/ - Test validation
- POST /detect-fraud-from-pdf/ - AI fraud detection
```

---

## ⏭️ Next Steps

1. ✅ Test all endpoints in Swagger UI
2. ✅ Create test ZIP files to upload
3. ✅ Test PDF fraud detection
4. ✅ Show to hackathon judges!
5. ✅ Remember to STOP container after hackathon (to save money)

---

## 📞 Need Help?

**Common URLs:**
- Azure Portal: https://portal.azure.com
- Docker Hub: https://hub.docker.com
- Your API: Check Azure Portal → Container Instance → FQDN

**Check container status:**
1. Go to Azure Portal
2. Search for "Container Instances"
3. Click your container
4. Look at "Status" field

**View live logs:**
1. Container Instance → Containers → Logs

Good luck with your hackathon! 🎊

---

## 🗑️ Clean Up (After Hackathon)

### To delete everything and stop charges:

1. Go to Azure Portal
2. Click "Resource groups" in left menu
3. Click on `metlife-rg`
4. Click "Delete resource group" at the top
5. Type the resource group name to confirm
6. Click "Delete"

This will delete:
- Container Instance
- All associated resources
- Stop all charges

**Your Docker image on Docker Hub will remain** (free forever)

---

## 💡 Pro Tips

1. **Save money**: Stop container when not using
2. **Quick updates**: Just rebuild & push Docker image, then restart container
3. **Monitor logs**: Always check logs if something doesn't work
4. **Test locally first**: Run `docker run` before pushing to Azure
5. **Free credits**: Use all $200 before it expires!

**Estimated cost with $200 credit:**
- Can run 24/7 for ~6 months
- Or run part-time for much longer!

---

**Ready to deploy? Start with Part 1! 🚀**
