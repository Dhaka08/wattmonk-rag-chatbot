import streamlit as st
import os
from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.chatbot import RAGChatbot

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Wattmonk AI Assistant",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .nec-badge {
        background-color: #fff3cd;
        color: #856404;
    }
    .wattmonk-badge {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .general-badge {
        background-color: #d4edda;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_system():
    """Initialize the RAG system (cached to avoid reloading)"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found in .env file")
        st.stop()
    
    # Process documents
    with st.spinner("📚 Loading documents..."):
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        documents = processor.process_documents("data")
    
    # Initialize vector store
    with st.spinner("🔍 Building vector database..."):
        vector_store = VectorStore(api_key)
        vector_store.add_documents(documents)
    
    # Initialize chatbot
    chatbot = RAGChatbot(api_key, vector_store)
    
    return chatbot, documents

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot, st.session_state.documents = initialize_system()

# Header
st.markdown('<h1 class="main-header">⚡ Wattmonk AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent companion for NEC codes and Wattmonk information</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 System Info")
    
    # Document stats
    nec_count = len(st.session_state.documents['nec'])
    wattmonk_count = len(st.session_state.documents['wattmonk'])
    
    st.metric("NEC Code Chunks", nec_count)
    st.metric("Wattmonk Info Chunks", wattmonk_count)
    
    st.divider()
    
    st.header("💡 Capabilities")
    st.write("✅ Answer general questions")
    st.write("✅ Explain NEC electrical codes")
    st.write("✅ Provide Wattmonk company info")
    st.write("✅ Context-aware responses")
    st.write("✅ Search across documents")
    st.write("✅ Page-level citations")
    
    st.divider()
    
    st.header("🎯 Example Queries")
    example_queries = [
        "What is the NEC code for grounding?",
        "Tell me about Wattmonk services",
        "What is the voltage requirement for circuits?",
        "What does Wattmonk specialize in?"
    ]
    
    for example in example_queries:
        if st.button(example, key=example):
            st.session_state.user_input = example
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        st.rerun()

# Search functionality
st.divider()
with st.expander("🔍 Search Documents", expanded=False):
    search_query = st.text_input("Search across all documents:", placeholder="e.g., grounding requirements")
    
    if st.button("Search", type="primary"):
        if search_query:
            with st.spinner("Searching..."):
                results = st.session_state.chatbot.vector_store.search_all(search_query, n_results=5)
                
                if results:
                    st.success(f"Found {len(results)} results")
                    for i, result in enumerate(results, 1):
                        with st.container():
                            st.markdown(f"**Result {i}** - {result['source']} (Page {result.get('page', 'Unknown')})")
                            st.text(result['text'][:300] + "..." if len(result['text']) > 300 else result['text'])
                            st.divider()
                else:
                    st.warning("No results found. Try different keywords.")

st.divider()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and "source" in message:
            intent = message.get("intent", "general")
            badge_class = f"{intent}-badge"
            page_info = message.get("pages", "")
            source_text = f"📚 Source: {message['source']}"
            if page_info:
                source_text += f" | {page_info}"
            st.markdown(
                f'<span class="source-badge {badge_class}">{source_text}</span>',
                unsafe_allow_html=True
            )

# Chat input
if prompt := st.chat_input("Ask me anything about NEC codes, Wattmonk, or general topics..."):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.chatbot.generate_response(prompt)
            
            st.write(result["response"])
            
            # Display source badge with page info
            intent = result["intent"]
            badge_class = f"{intent}-badge"
            page_info = result.get("pages", "")
            source_text = f"📚 Source: {result['source']}"
            if page_info:
                source_text += f" | {page_info}"
            st.markdown(
                f'<span class="source-badge {badge_class}">{source_text}</span>',
                unsafe_allow_html=True
            )
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "source": result["source"],
        "intent": result["intent"],
        "pages": result.get("pages", "")
    })

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with ❤️ for Wattmonk Technologies | Powered by Google Gemini AI
    </div>
    """,
    unsafe_allow_html=True
)