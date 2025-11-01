# Quick Docker Build and Test Script
# Run this file: .\docker-quick-start.ps1

Write-Host "=== MetLife Claim Fraud API - Docker Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build Docker Image
Write-Host "[1/4] Building Docker image..." -ForegroundColor Yellow
docker build -t claim-fraud-api:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Stop any existing containers
Write-Host "[2/4] Stopping existing containers..." -ForegroundColor Yellow
docker stop claim-fraud-api-test 2>$null
docker rm claim-fraud-api-test 2>$null
Write-Host "✅ Cleaned up old containers" -ForegroundColor Green
Write-Host ""

# Step 3: Run Docker Container
Write-Host "[3/4] Starting Docker container..." -ForegroundColor Yellow
docker run -d `
  --name claim-fraud-api-test `
  -p 8000:8000 `
  -e PORT=8000 `
  -e GEMINI_API_KEY=AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0 `
  claim-fraud-api:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start container!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Container started successfully!" -ForegroundColor Green
Write-Host ""

# Step 4: Wait for API to be ready
Write-Host "[4/4] Waiting for API to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

$maxRetries = 10
$retryCount = 0
$apiReady = $false

while ($retryCount -lt $maxRetries -and -not $apiReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $apiReady = $true
        }
    } catch {
        $retryCount++
        Write-Host "  Attempt $retryCount/$maxRetries..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
if ($apiReady) {
    Write-Host "✅ API is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=== 🚀 YOUR API IS RUNNING! ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📍 API URL:      http://localhost:8000" -ForegroundColor White
    Write-Host "📖 API Docs:     http://localhost:8000/docs" -ForegroundColor White
    Write-Host "🔍 Health Check: http://localhost:8000/" -ForegroundColor White
    Write-Host ""
    Write-Host "=== Useful Commands ===" -ForegroundColor Cyan
    Write-Host "View logs:       docker logs -f claim-fraud-api-test" -ForegroundColor Gray
    Write-Host "Stop container:  docker stop claim-fraud-api-test" -ForegroundColor Gray
    Write-Host "Restart:         docker restart claim-fraud-api-test" -ForegroundColor Gray
    Write-Host "Remove:          docker rm -f claim-fraud-api-test" -ForegroundColor Gray
    Write-Host ""
    
    # Open browser
    Write-Host "Opening API documentation in browser..." -ForegroundColor Yellow
    Start-Process "http://localhost:8000/docs"
    
} else {
    Write-Host "❌ API failed to start. Check logs with:" -ForegroundColor Red
    Write-Host "   docker logs claim-fraud-api-test" -ForegroundColor Yellow
    exit 1
}
