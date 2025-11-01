# 🎯 Azure Portal Deployment Checklist

**Print this or keep it open while deploying!**

---

## ✅ Pre-Deployment (5 minutes)

```powershell
# Run these commands in PowerShell:

# 1. Login to Docker Hub
docker login

# 2. Build image
docker build -t claim-fraud-api:latest .

# 3. Tag image (replace YOUR_USERNAME)
docker tag claim-fraud-api:latest YOUR_USERNAME/claim-fraud-api:latest

# 4. Push to Docker Hub
docker push YOUR_USERNAME/claim-fraud-api:latest
```

**✅ Done? Your image URL:** `YOUR_USERNAME/claim-fraud-api:latest`

---

## ✅ Azure Portal Steps (5 minutes)

### 1. Open Portal
- [ ] Go to [portal.azure.com](https://portal.azure.com)
- [ ] Sign in

### 2. Create Container
- [ ] Click "Create a resource"
- [ ] Search "Container Instances"
- [ ] Click "Create"

### 3. BASICS Tab
- [ ] Subscription: (select yours)
- [ ] Resource group: `metlife-rg` (create new)
- [ ] Container name: `claim-fraud-api`
- [ ] Region: `East US` (or closest)
- [ ] Image source: **Other registry**
- [ ] Image: `YOUR_USERNAME/claim-fraud-api:latest`
- [ ] CPU: `1` core
- [ ] Memory: `1.5` GiB
- [ ] Click "Next: Networking"

### 4. NETWORKING Tab
- [ ] Networking type: **Public**
- [ ] DNS name: `metlife-fraud-api` (any unique name)
- [ ] Port: `8000`
- [ ] Protocol: `TCP`
- [ ] Click "Next: Advanced"

### 5. ADVANCED Tab
- [ ] Restart policy: **Always**
- [ ] Add environment variable: `PORT` = `8000`
- [ ] Add environment variable: `GEMINI_API_KEY` = `AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0`
- [ ] Click "Review + create"

### 6. Deploy
- [ ] Review settings
- [ ] Click "Create"
- [ ] Wait 2-3 minutes
- [ ] Click "Go to resource"

### 7. Get URL
- [ ] Copy the FQDN (your API URL)
- [ ] Add `:8000/docs` to the end
- [ ] Open in browser

---

## ✅ Test Your API

**Your API URL format:**
```
http://metlife-fraud-api.[region].azurecontainer.io:8000
```

### Quick Tests:
- [ ] Open: `http://your-url:8000/` (should show welcome message)
- [ ] Open: `http://your-url:8000/docs` (should show Swagger UI)
- [ ] Test an endpoint in Swagger UI

---

## ✅ Verification Checklist

**In Azure Portal:**
- [ ] Container Status: **Running** (green checkmark)
- [ ] Provisioning State: **Succeeded**
- [ ] Logs show: "Uvicorn running on..."

**In Browser:**
- [ ] API docs page loads
- [ ] Can see all 3 endpoints
- [ ] Can try out endpoints

---

## 🐛 If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Container not starting | Check logs in Azure Portal |
| Can't access URL | Make sure it's `http://` not `https://` |
| Port error | Verify port is `8000` in networking |
| Image not found | Check Docker Hub - is image public? |
| Tesseract error | Rebuild Docker image with our Dockerfile |

---

## 💰 Cost Tracking

**Running 24/7:** ~$34/month  
**Your $200 credit:** Lasts ~6 months

**To save money:**
- Stop container when not using: Overview → Stop
- Start again when needed: Overview → Start

---

## 📊 Important URLs

| What | URL |
|------|-----|
| Azure Portal | https://portal.azure.com |
| Docker Hub | https://hub.docker.com |
| Your Resource Group | portal.azure.com → Resource groups → metlife-rg |
| Your Container | portal.azure.com → Container Instances → claim-fraud-api |

---

## 🎉 Success Criteria

✅ Container shows "Running" status  
✅ Can access API docs at `/docs`  
✅ All 3 endpoints visible in Swagger UI  
✅ Can upload a file and get response  

**You're live! 🚀**

---

## 🗑️ Clean Up After Hackathon

1. Portal → Resource groups
2. Click `metlife-rg`
3. Delete resource group
4. Confirm deletion

**This stops all charges immediately!**

---

## 📝 Quick Notes Space

**My Docker Hub username:** ________________

**My image name:** ________________/claim-fraud-api:latest

**My Azure URL:** http://________________.azurecontainer.io:8000

**My API Key:** AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0

---

**Good luck! 🍀**
