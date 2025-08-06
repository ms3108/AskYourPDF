@echo off
echo Starting Ollama with Docker...
docker run -d --name ollama -p 11434:11434 -v ollama_data:/root/.ollama -e OLLAMA_HOST=0.0.0.0 ollama/ollama:latest

echo Waiting for Ollama to start...
timeout /t 10

echo Pulling a model (llama3.2 - a good default model)...
docker exec ollama ollama pull llama3.2

echo Setup complete! Ollama is running on http://localhost:11434
echo You can now start your Flask app and it should connect to Ollama
pause
