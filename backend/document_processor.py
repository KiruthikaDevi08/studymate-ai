from sentence_transformers import SentenceTransformer
import numpy as np

class DocumentProcessor:
    def __init__(self):
        self.chunks = []
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def load_document(self, file_path):
        try:
            print(f"Reading file: {file_path}")  # Debug line
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            print(f"File content length: {len(text)}")  # Debug line
            self.chunks = self._chunk_text(text)
            print(f"Created {len(self.chunks)} chunks")  # Debug line
            self.embeddings = self.model.encode(self.chunks)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
            
    def _chunk_text(self, text, chunk_size=50):  # Smaller chunks
        # First split by lines to preserve section boundaries
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            if line.strip():  # If line has content
                current_chunk.append(line.strip())
                # If we have enough content, create a chunk
                if len(' '.join(current_chunk).split()) >= chunk_size:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
        
        # Add any remaining content
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks
    
    def find_relevant_chunks(self, question, top_k=5):  # Increased to 5
        if not self.chunks:
            return []
        question_embedding = self.model.encode([question])
        similarities = np.dot(self.embeddings, question_embedding.T).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # Filter chunks that actually contain question keywords
        question_keywords = set(question.lower().split())
        relevant_chunks = []
        for i in top_indices:
            chunk_text = self.chunks[i].lower()
            # Check if chunk contains any substantial keywords from question
            if any(len(keyword) > 3 and keyword in chunk_text for keyword in question_keywords):
                relevant_chunks.append(self.chunks[i])
        
        return relevant_chunks[:3]  # Return top 3 truly relevant chunks