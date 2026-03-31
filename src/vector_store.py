from typing import List, Dict
import os

class VectorStore:
    def __init__(self, api_key: str):
        # Store documents in memory
        self.nec_documents = []
        self.wattmonk_documents = []
    
    def add_documents(self, documents: Dict[str, List[Dict]]):
        """Add documents to storage"""
        if documents['nec']:
            self.nec_documents = documents['nec']
            print(f"✅ Loaded {len(self.nec_documents)} NEC chunks")
        
        if documents['wattmonk']:
            self.wattmonk_documents = documents['wattmonk']
            print(f"✅ Loaded {len(self.wattmonk_documents)} Wattmonk chunks")
    
    def simple_search(self, query: str, documents: List[Dict], n_results: int = 3) -> List[Dict]:
        """Simple keyword-based search"""
        query_words = set(query.lower().split())
        
        # Score each document
        scored_docs = []
        for doc in documents:
            doc_words = set(doc['text'].lower().split())
            # Calculate overlap score
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0:
                scored_docs.append((overlap, doc))
        
        # Sort by score and return top results
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:n_results]]
    
    def search(self, query: str, collection_type: str, n_results: int = 3) -> Dict:
        """Search for relevant documents"""
        if collection_type == "nec":
            docs = self.simple_search(query, self.nec_documents, n_results)
        elif collection_type == "wattmonk":
            docs = self.simple_search(query, self.wattmonk_documents, n_results)
        else:
            return {'documents': [[]], 'metadatas': [[]], 'pages': [[]]}
        
        if not docs:
            return {'documents': [[]], 'metadatas': [[]], 'pages': [[]]}
        
        # Format results with page numbers
        results = {
            'documents': [[doc['text'] for doc in docs]],
            'metadatas': [[{
                'source': doc['source'], 
                'chunk_id': doc['chunk_id'],
                'page': doc.get('page', 'Unknown')
            } for doc in docs]],
            'pages': [[doc.get('page', 'Unknown') for doc in docs]]
        }
        
        return results
    
    def search_all(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search across all documents for the search feature"""
        all_docs = self.nec_documents + self.wattmonk_documents
        return self.simple_search(query, all_docs, n_results)