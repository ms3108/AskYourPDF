Write-Host "Starting Ollama and AskYourPDF with Docker Compose..." -ForegroundColor Green

# Start the services
Write-Host "Running docker-compose up -d..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to start
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check if containers are running
Write-Host "Checking container status..." -ForegroundColor Yellow
docker ps

# Pull a model for Ollama
Write-Host "Pulling llama3.2 model for Ollama..." -ForegroundColor Yellow
docker exec ollama ollama pull llama3.2

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Ollama is available at: http://localhost:11434" -ForegroundColor Cyan
Write-Host "Your Flask app is available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Health check endpoint: http://localhost:5000/health" -ForegroundColor Cyan
