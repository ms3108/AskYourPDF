# AskYourPDF

A Flask-based web application that allows users to upload PDF documents and ask questions about their content using AI-powered responses via Ollama.

## Features

- 📄 **PDF Upload**: Upload and process PDF documents
- 🤖 **AI Q&A**: Ask questions about your uploaded documents
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 🔍 **Health Monitoring**: Built-in health check endpoints
- 🎨 **Modern UI**: Clean, responsive interface with Tailwind CSS

## Quick Start

### Method 1: Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/ms3108/AskYourPDF.git
cd AskYourPDF
```

2. Start the services:
```bash
docker-compose up -d
```

3. Pull an AI model for Ollama:
```bash
docker exec ollama ollama pull llama3.2
```

4. Access the application at `http://localhost:5000`

### Method 2: Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Ollama separately:
```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama:latest
docker exec ollama ollama pull llama3.2
```

3. Run the Flask app:
```bash
python app.py
```

## Usage

1. **Upload a PDF**: Navigate to `http://localhost:5000` and upload your PDF document
2. **Ask Questions**: Once uploaded, you can ask questions about the document content
3. **Get AI Responses**: The system uses Ollama to provide intelligent answers based on the document

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Upload PDF documents
- `GET /qa/<filename>` - Q&A interface for uploaded documents
- `POST /ask` - Submit questions about documents
- `GET /health` - Health check endpoint
- `POST /reset` - Reset current session

## Configuration

The application can be configured through environment variables:

- `OLLAMA_API_URL` - Ollama API endpoint (default: `http://ollama:11434`)
- `UPLOAD_FOLDER` - Directory for uploaded files (default: `uploads`)
- `MAX_CONTENT_LENGTH` - Maximum file upload size (default: 16MB)

## Requirements

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- Ollama (for AI responses)

## Supported Models

The application works with various Ollama models:
- `llama3.2` - General purpose model (recommended)
- `llama3.2:1b` - Lightweight version
- `qwen2.5:7b` - Alternative high-quality model

## Development

To run in development mode:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with debug mode
python app.py
```

The application will be available at `http://localhost:5000` with debug mode enabled.

## License

This project is open source and available under the [MIT License](LICENSE).
