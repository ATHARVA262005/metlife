# Deploying to Render

This guide will help you deploy your Claim Fraud Detection API to Render.

## Prerequisites

1. A [Render](https://render.com/) account (free tier available)
2. Your GitHub repository pushed to GitHub
3. Google Gemini API key

## Important Note About Tesseract OCR

⚠️ **Tesseract OCR Limitation on Render**: 
The `/detect-fraud-from-pdf/` endpoint requires Tesseract OCR, which needs system-level installation. Render's free tier doesn't support custom system packages easily. 

**Options:**
1. **Use only JSON validation endpoints** (`/validate-zip-claim/` and `/validate-local-folder/`)
2. **Upgrade to Render paid plan** with Docker support
3. **Deploy to a different platform** (Railway, Heroku, DigitalOcean) that supports apt packages

## Deployment Steps

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Push your code to GitHub** (you've already done this!)
   ```bash
   git push -u origin main
   ```

2. **Log in to Render**
   - Go to [dashboard.render.com](https://dashboard.render.com/)
   - Sign up or log in with GitHub

3. **Create a New Web Service**
   - Click "New +" button → "Web Service"
   - Connect your GitHub repository: `ATHARVA262005/metlife`
   - Select the repository

4. **Configure the Service**
   - **Name**: `claim-fraud-detection-api` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank (or `3` if your repo has multiple folders)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables** (Important!)
   - Click "Advanced" → "Add Environment Variable"
   - Add these:
     - `PYTHON_VERSION` = `3.12.0`
     - `GEMINI_API_KEY` = `AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0` (your actual key)

6. **Choose Free Plan** (or paid if you need Tesseract)
   - Select "Free" plan
   - Click "Create Web Service"

7. **Wait for Deployment**
   - Render will build and deploy (takes 3-5 minutes)
   - You'll get a URL like: `https://claim-fraud-detection-api.onrender.com`

### Option 2: Deploy with Blueprint (render.yaml)

1. **Use the render.yaml file** (already created in this repo)
   
2. **Create New Blueprint**
   - In Render Dashboard → "New +" → "Blueprint"
   - Connect GitHub repo
   - Render will auto-detect `render.yaml`
   - Add environment variables in dashboard
   - Deploy!

## Testing Your Deployed API

Once deployed, test your endpoints:

### 1. Check API is running
```bash
curl https://your-app-name.onrender.com/
```

### 2. Test ZIP validation
```bash
curl -X POST "https://your-app-name.onrender.com/validate-zip-claim/" \
  -F "file=@claim_folder_001.zip"
```

### 3. Access API Documentation
Open in browser:
```
https://your-app-name.onrender.com/docs
```

## Limitations on Free Tier

1. **Cold Starts**: Free tier sleeps after 15 minutes of inactivity (first request takes 30-60 seconds)
2. **No Tesseract**: PDF OCR endpoint won't work without system packages
3. **750 hours/month**: Free tier limit
4. **512 MB RAM**: May be tight for large PDFs

## Working Endpoints on Free Tier

✅ `/` - Root endpoint
✅ `/validate-zip-claim/` - Upload ZIP of JSON files
✅ `/validate-local-folder/` - Validate local folders (if you upload datasets)
✅ `/docs` - Interactive API documentation

❌ `/detect-fraud-from-pdf/` - Requires Tesseract (won't work on free tier)

## Alternative: Deploy with Docker (Paid Tier)

If you need the PDF OCR endpoint, you can use Docker:

### 1. Create Dockerfile
```dockerfile
FROM python:3.12-slim

# Install system dependencies including Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Deploy Docker on Render
- Choose "Docker" runtime in Render
- Render will build from Dockerfile
- This requires paid plan ($7/month)

## Update Your Code for Production

### Make Port Dynamic
Your code already handles this correctly:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

But for Render, update to:
```python
import os
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Remove API Key from Code
Don't hardcode API keys! Use environment variables:
```python
gemini_api_key: str = Query(
    default=os.environ.get("GEMINI_API_KEY"),
    description="Your Google Gemini API key"
)
```

## Troubleshooting

### Build fails
- Check Python version in requirements.txt
- Make sure all dependencies are listed
- Check Render build logs

### App crashes on start
- Check start command is correct
- Verify PORT environment variable
- Check app logs in Render dashboard

### Endpoints return 500 errors
- Check environment variables are set
- Verify API keys are valid
- Check app logs for errors

## Cost Estimate

- **Free Tier**: $0/month (no PDF OCR)
- **Starter**: $7/month (includes Docker, 512MB RAM)
- **Standard**: $25/month (2GB RAM, better for PDFs)

## Next Steps

1. Push code to GitHub ✅ (Done!)
2. Sign up for Render
3. Connect GitHub repository
4. Configure environment variables
5. Deploy and test
6. Share your API URL!

## Support

- Render Docs: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Contact: Check Render support or community forum
