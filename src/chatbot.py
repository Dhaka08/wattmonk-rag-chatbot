from google import genai
from typing import List, Dict, Tuple
import os

class RAGChatbot:
    def __init__(self, api_key: str, vector_store):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.5-flash'
        self.vector_store = vector_store
        self.conversation_history = []
    
    def classify_intent(self, query: str) -> str:
        """Classify user query intent"""
        query_lower = query.lower()
        
        # NEC related keywords
        nec_keywords = ['nec', 'electrical code', 'wiring', 'circuit', 'voltage', 
                       'ampere', 'amp', 'grounding', 'conductor', 'panel', 'breaker',
                       'electrical', 'installation', 'regulation', 'standard', 'wire',
                       'conduit', 'outlet', 'switch', 'ground', 'neutral', 'phase']
        
        # Wattmonk related keywords
        wattmonk_keywords = ['wattmonk', 'company', 'service', 'team', 'policy',
                            'about us', 'contact', 'pricing', 'solar', 'design',
                            'about you', 'who are you', 'what do you do']
        
        # Check for NEC keywords
        if any(keyword in query_lower for keyword in nec_keywords):
            return "nec"
        
        # Check for Wattmonk keywords
        if any(keyword in query_lower for keyword in wattmonk_keywords):
            return "wattmonk"
        
        # Default to general conversation
        return "general"
    
    def get_relevant_context(self, query: str, intent: str) -> Tuple[str, str, List[int]]:
        """Retrieve relevant context from vector store"""
        if intent == "general":
            return "", "Base Knowledge", []
        
        results = self.vector_store.search(query, intent, n_results=3)
        
        if not results['documents'] or not results['documents'][0]:
            return "", "No specific context found", []
        
        # Combine retrieved documents with page numbers
        context_parts = []
        pages = []
        
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            page_num = metadata.get('page', 'Unknown')
            pages.append(page_num)
            context_parts.append(f"[Page {page_num}]\n{doc}")
        
        context = "\n\n".join(context_parts)
        source = results['metadatas'][0][0]['source'] if results['metadatas'] else intent.upper()
        
        return context, source, pages
    
    def generate_response(self, query: str) -> Dict[str, str]:
        """Generate chatbot response using RAG"""
        
        # Classify intent
        intent = self.classify_intent(query)
        
        # Get relevant context
        context, source, pages = self.get_relevant_context(query, intent)
        
        # Build prompt
        if intent == "general":
            prompt = f"You are a helpful AI assistant. Answer this question naturally and conversationally:\n\n{query}"
        else:
            if context and context != "":
                prompt = f"""You are a helpful assistant that answers questions based on provided context from technical documents.

Context from {source}:
{context}

Question: {query}

Instructions:
- Answer based on the context above
- Be specific and cite the page numbers when relevant
- If the context doesn't fully answer the question, say what you found and what's missing
- Be helpful and professional

Answer:"""
            else:
                # Fallback when no context found
                prompt = f"""The user asked: "{query}"

This question seems related to {intent.upper()} but I couldn't find specific information in the available documents.

Provide a helpful response that:
1. Acknowledges you don't have specific information from the documents
2. Offers to help with related questions you might be able to answer
3. Suggests what kind of information would be in {intent.upper()} documents

Be polite and helpful."""
        
        # Call Gemini API
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
                )
            assistant_message = response.text
        except Exception as e:
            assistant_message = f"I apologize, but I encountered an error generating a response. Please try rephrasing your question or ask something else. Error: {str(e)}"
        
        # Format page numbers for display
        page_info = ""
        if pages:
            unique_pages = sorted(set(pages))
            if len(unique_pages) == 1:
                page_info = f"Page {unique_pages[0]}"
            else:
                page_info = f"Pages {', '.join(map(str, unique_pages))}"
        
        return {
            "response": assistant_message,
            "intent": intent,
            "source": source,
            "pages": page_info
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []