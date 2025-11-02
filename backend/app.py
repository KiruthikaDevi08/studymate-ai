from flask import Flask, request, jsonify
from document_processor import DocumentProcessor
import os
from flask_cors import CORS  # Add this line

 
app = Flask(__name__)
CORS(app) 
doc_processor = DocumentProcessor()

@app.route('/')
def hello():
    return "StudyMate AI is working!"

@app.route('/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"File received: {file.filename}, Size: {file.content_length}")  # Add this line
        
        # Save and process the file
        uploads_dir = 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        filename = os.path.join(uploads_dir, file.filename)
        file.save(filename)
        
        print(f"File saved to: {os.path.abspath(filename)}")
        
        # Check if file actually has content
        with open(filename, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            print(f"Saved file content length: {len(saved_content)}")  # Add this line
        
        # Process document
        success = doc_processor.load_document(filename)
        print(f"Processing success: {success}, Chunks: {len(doc_processor.chunks)}")
        
        if success:
            return jsonify({'message': f'Document {file.filename} uploaded successfully!', 'status': 'success'})
        else:
            return jsonify({'error': 'Failed to process document'}), 500
            
    except Exception as e:
        print(f"Upload error: {e}")  # Add this line
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "No question provided"})
        
        relevant_chunks = doc_processor.find_relevant_chunks(question)
        
        if not relevant_chunks:
            answer = "I couldn't find specific information about that in your notes."
        else:
            # Just return the most relevant chunk
            answer = "Based on your notes:\n" + relevant_chunks[0]
        
        return jsonify({"answer": answer, "status": "success"})
        
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)