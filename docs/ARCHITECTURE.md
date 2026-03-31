# 🏗️ System Architecture

## Overview

The Wattmonk RAG Chatbot uses a multi-layered architecture combining document processing, intelligent retrieval, and large language model generation to provide accurate, context-aware responses.

## High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                      (Streamlit Web App)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   app.py     │  │  Session     │  │   UI State   │     │
│  │  (Main App)  │  │  Management  │  │  Management  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              1. Query Processing                      │  │
│  │  ┌────────────────┐      ┌─────────────────┐        │  │
│  │  │ Intent         │─────▶│ Keyword         │        │  │
│  │  │ Classification │      │ Extraction      │        │  │
│  │  └────────────────┘      └─────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            2. Document Retrieval                      │  │
│  │  ┌────────────────┐      ┌─────────────────┐        │  │
│  │  │ Vector Store   │─────▶│ Similarity      │        │  │
│  │  │ Query          │      │ Search          │        │  │
│  │  └────────────────┘      └─────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           3. Context Preparation                      │  │
│  │  ┌────────────────┐      ┌─────────────────┐        │  │
│  │  │ Context        │─────▶│ Prompt          │        │  │
│  │  │ Aggregation    │      │ Construction    │        │  │
│  │  └────────────────┘      └─────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            4. Response Generation                     │  │
│  │  ┌────────────────┐      ┌─────────────────┐        │  │
│  │  │ Google Gemini  │─────▶│ Response        │        │  │
│  │  │ API Call       │      │ Formatting      │        │  │
│  │  └────────────────┘      └─────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  NEC Code    │  │  Wattmonk    │  │  In-Memory   │     │
│  │  Documents   │  │  Documents   │  │  Vector Store│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer (Streamlit)

**File**: `app.py`

**Responsibilities**:
- Render chat interface
- Handle user input
- Display responses with formatting
- Manage search functionality
- Show document statistics
- Provide example queries

**Key Features**:
- Real-time streaming responses
- Session state management
- Responsive design
- Custom CSS styling

### 2. Document Processing Layer

**File**: `src/document_processor.py`

**Class**: `DocumentProcessor`

**Responsibilities**:
- Extract text from PDF documents
- Split text into manageable chunks
- Maintain metadata (source, page number)
- Handle tokenization

**Process Flow**:
```
PDF File → Text Extraction → Tokenization → Chunking → Metadata Addition
```

**Configuration**:
- Chunk size: 500 tokens
- Chunk overlap: 50 tokens
- Encoding: cl100k_base (tiktoken)

### 3. Vector Store Layer

**File**: `src/vector_store.py`

**Class**: `VectorStore`

**Responsibilities**:
- Store processed document chunks
- Perform similarity search
- Manage separate collections (NEC vs Wattmonk)
- Return relevant context with metadata

**Search Algorithm**:
```python
1. Tokenize query into keywords
2. For each document:
   - Tokenize document text
   - Calculate keyword overlap score
   - Store (score, document) pair
3. Sort by score (descending)
4. Return top N results
```

**Storage Structure**:
```
{
  'nec': [
    {
      'text': '...',
      'source': 'NEC Code',
      'page': 42,
      'chunk_id': 0
    },
    ...
  ],
  'wattmonk': [...]
}
```

### 4. Chatbot Logic Layer

**File**: `src/chatbot.py`

**Class**: `RAGChatbot`

**Responsibilities**:
- Classify user intent
- Retrieve relevant context
- Construct prompts
- Call LLM API
- Format responses
- Handle fallbacks

**Intent Classification**:
```python
Query → Keyword Matching → Intent Label
                            ↓
                    [nec | wattmonk | general]
```

**Keywords**:
- **NEC**: electrical code, wiring, circuit, voltage, grounding, etc.
- **Wattmonk**: company, service, solar, design, policy, etc.
- **General**: Everything else

**Prompt Construction**:

For domain-specific queries:
```
System: You are a helpful assistant...

Context from [SOURCE]:
[Retrieved documents with page numbers]

Question: [User query]

Instructions: [Answer guidelines]
```

For general queries:
```
System: You are a helpful AI assistant...

Question: [User query]
```

### 5. LLM Integration

**Provider**: Google Gemini

**Model**: `gemini-2.5-flash`

**Configuration**:
- Temperature: Default
- Max tokens: Default
- Streaming: No

**API Call Flow**:
```
Prompt → Gemini API → Response Text → Post-processing → Display
```

## Data Flow

### Query Processing Flow
```
1. User enters query
   ↓
2. Intent classification (NEC/Wattmonk/General)
   ↓
3. If domain-specific:
   → Retrieve relevant chunks (top 3)
   → Extract page numbers
   → Build context string
   ↓
4. Construct prompt with context
   ↓
5. Call Gemini API
   ↓
6. Parse response
   ↓
7. Add source attribution and page numbers
   ↓
8. Display to user
```

### Document Loading Flow
```
1. App starts → Initialize system (cached)
   ↓
2. Scan data/ folder for PDFs
   ↓
3. For each PDF:
   → Extract text per page
   → Classify as NEC or Wattmonk
   → Chunk text with overlap
   → Store with metadata
   ↓
4. Build in-memory vector store
   ↓
5. Initialize chatbot with vector store
   ↓
6. Ready for queries
```

## Technology Stack Details

### Frontend Technologies
- **Streamlit 1.31.0**: Web framework
- **Custom CSS**: Styling
- **Session State**: State management

### Backend Technologies
- **Python 3.9+**: Core language
- **Google GenerativeAI SDK**: LLM integration
- **PyPDF**: PDF text extraction
- **Tiktoken**: Tokenization

### Data Processing
- **In-memory storage**: Fast retrieval
- **Keyword-based search**: Simple and effective
- **Token-based chunking**: Consistent chunk sizes

## Security Architecture

### API Key Management
```
.env file (not in Git) → Environment variables → Application
```

### Data Privacy
- No logging of user queries
- No external data transmission (except to Gemini API)
- Local document processing
- Session-based state (no persistence)

## Performance Considerations

### Optimization Strategies
1. **Caching**: Document processing cached with `@st.cache_resource`
2. **In-memory storage**: Fast retrieval without database overhead
3. **Lightweight search**: Keyword matching vs vector similarity
4. **Efficient chunking**: Optimal token size for context windows

### Scalability Limits
- **Document size**: Limited by available RAM
- **Concurrent users**: Single-threaded Streamlit app
- **API rate limits**: Gemini API quotas

### Recommended Improvements for Production
1. Replace in-memory store with proper vector database (Pinecone/Weaviate)
2. Add Redis for session management
3. Implement request queuing
4. Add response caching
5. Use asynchronous API calls

## Error Handling

### Levels of Error Handling

1. **Input Validation**
   - Check for empty queries
   - Validate API key presence

2. **Processing Errors**
   - PDF parsing failures
   - Tokenization errors
   - Graceful degradation

3. **API Errors**
   - Rate limit handling
   - Network timeout handling
   - Fallback responses

4. **User-Facing Errors**
   - Clear error messages
   - Suggestions for resolution
   - No technical jargon

## Monitoring and Logging

### Current Implementation
- Document count displayed in sidebar
- Search result counts
- Basic error messages in UI

### Recommended Additions
- Query latency tracking
- API usage metrics
- Error rate monitoring
- User interaction analytics

## Future Architecture Enhancements

### Short-term
1. Add proper vector database (ChromaDB/Pinecone)
2. Implement conversation memory persistence
3. Add response caching
4. Improve search algorithm

### Long-term
1. Multi-model support (GPT-4, Claude, etc.)
2. Advanced RAG techniques (HyDE, ReAct)
3. Fine-tuned embeddings
4. Real-time document updates
5. Multi-user support with authentication
6. Advanced analytics dashboard

---

**Last Updated**: March 31, 2026  
**Version**: 1.0.0