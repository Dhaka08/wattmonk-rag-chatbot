import os
from pypdf import PdfReader
from typing import List, Dict

class DocumentProcessor:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size  # characters instead of tokens
        self.chunk_overlap = chunk_overlap
    
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
        """Split text into chunks by character count"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                "text": chunk_text,
                "source": source,
                "page": page_num,
                "chunk_id": len(chunks)
            })
            
            start = end - self.chunk_overlap
        
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