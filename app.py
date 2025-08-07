from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import requests
import json
from werkzeug.utils import secure_filename
import PyPDF2
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}
OLLAMA_API_URL = "http://ollama:11434"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def query_llama(question, context):
    """Query Llama model with context"""
    try:
        # Limit context to avoid token limits
        limited_context = context[:3000] if len(context) > 3000 else context
        
        prompt = f"""Based on the following document content, please answer the question. If the answer is not found in the document, please say so.

Document Content:
{limited_context}

Question: {question}

Answer:"""

        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500
            }
        }
        
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'No response received')
        else:
            return f"Error querying model: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}. Make sure Ollama is running."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Upload route called")
        
        if 'file' not in request.files:
            print("No file in request")
            flash('No file selected')
            return redirect(url_for('index'))
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Empty filename")
            flash('No file selected')
            return redirect(url_for('index'))
        
        if not file or not allowed_file(file.filename):
            print(f"File not allowed: {file.filename}")
            flash('Invalid file type. Please upload a PDF file.')
            return redirect(url_for('index'))
            
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {file_path}")
        
        file.save(file_path)
        print("File saved successfully")
        
        # Extract text from PDF
        text_content = extract_text_from_pdf(file_path)
        print(f"Text extraction result: {'Success' if text_content else 'Failed'}")
        
        if text_content:
            # Store text content in session
            session['document_content'] = text_content
            session['filename'] = filename
            flash(f'PDF "{filename}" uploaded and processed successfully!')
            return redirect(url_for('qa_interface'))
        else:
            flash('Error extracting text from PDF. Please make sure it\'s a valid PDF with readable text.')
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"Upload error: {str(e)}")
        flash(f'An error occurred during upload: {str(e)}')
        return redirect(url_for('index'))

@app.route('/qa')
def qa_interface():
    if 'document_content' not in session:
        flash('Please upload a PDF first')
        return redirect(url_for('index'))
    
    return render_template('qa.html', filename=session.get('filename', 'Unknown'))

@app.route('/ask', methods=['POST'])
def ask_question():
    if 'document_content' not in session:
        flash('Please upload a PDF first')
        return redirect(url_for('index'))
    
    question = request.form.get('question', '').strip()
    if not question:
        flash('Please enter a question')
        return redirect(url_for('qa_interface'))
    
    # Query the Llama model
    answer = query_llama(question, session['document_content'])
    
    return render_template('qa.html', 
                         filename=session.get('filename', 'Unknown'),
                         question=question,
                         answer=answer)

@app.route('/reset')
def reset():
    session.clear()
    # Clean up uploaded files (optional)
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            pass
    flash('Session reset successfully')
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        ollama_status = "disconnected"
    
    return {
        "status": "healthy",
        "ollama": ollama_status
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)