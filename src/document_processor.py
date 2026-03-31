import os
from pypdf import PdfReader
from typing import List, Dict
import tiktoken

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract text from PDF file with page numbers"""
        reader = PdfReader(pdf_path)
        pages_data = []
        
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text.strip():
                pages_data.append({
                    "text": text,
                    "page": page_num
                })
        
        return pages_data
    
    def chunk_text(self, text: str, source: str, page_num: int) -> List[Dict]:
        """Split text into chunks with metadata"""
        tokens = self.encoding.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append({
                "text": chunk_text,
                "source": source,
                "page": page_num,
                "chunk_id": len(chunks)
            })
        
        return chunks
    
    def process_documents(self, data_folder: str) -> Dict[str, List[Dict]]:
        """Process all documents in the data folder"""
        documents = {
            "nec": [],
            "wattmonk": []
        }
        
        for filename in os.listdir(data_folder):
            if filename.endswith('.pdf'):
                filepath = os.path.join(data_folder, filename)
                pages_data = self.extract_text_from_pdf(filepath)
                
                # Determine document type based on filename
                if 'nec' in filename.lower() or '2017' in filename:
                    source = "nec"
                    doc_type = "NEC Code"
                elif 'wattmonk' in filename.lower():
                    source = "wattmonk"
                    doc_type = "Wattmonk Information"
                else:
                    source = "general"
                    doc_type = filename
                
                # Process each page
                for page_data in pages_data:
                    chunks = self.chunk_text(
                        page_data["text"], 
                        doc_type, 
                        page_data["page"]
                    )
                    documents[source].extend(chunks)
        
        return documents