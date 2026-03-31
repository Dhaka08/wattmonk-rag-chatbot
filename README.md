# ⚡ Wattmonk RAG Chatbot

An intelligent Retrieval-Augmented Generation (RAG) chatbot that provides context-aware answers from NEC electrical codes and Wattmonk company information, while maintaining conversational capabilities for general questions.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## 🎯 Features

- **Multi-Context Intelligence**: Seamlessly switches between NEC codes, Wattmonk information, and general knowledge
- **Source Attribution**: Citations with specific page numbers from source documents
- **Smart Search**: Cross-document search functionality
- **Context-Aware Responses**: RAG pipeline retrieves relevant information for accurate answers
- **Conversational Memory**: Maintains context across conversations
- **Fallback Handling**: Graceful responses when information is not available
- **Real-time Processing**: Instant responses with streaming interface

## 🏗️ Architecture
```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Intent Classifier│
│ (NEC/Wattmonk/  │
│   General)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Document Retrieval│
│ (Vector Search)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Context Injection│
│   into Prompt    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Google Gemini  │
│  (LLM Response) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Formatted Response│
│  with Citations  │
└─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Streamlit**: Interactive web interface with real-time chat

### Backend
- **Python 3.9+**: Core application logic
- **Google Gemini 2.5 Flash**: Large Language Model for response generation

### RAG Pipeline
- **Document Processing**: PyPDF for PDF text extraction
- **Text Chunking**: Token-based chunking with tiktoken
- **Vector Storage**: In-memory keyword-based search (lightweight alternative to vector DB)
- **Retrieval**: Smart keyword matching with scoring algorithm

### Additional Libraries
- `python-dotenv`: Environment variable management
- `google-generativeai`: Gemini API integration

## 📋 Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Git (for cloning the repository)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/wattmonk-rag-chatbot.git
cd wattmonk-rag-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Add Your Documents

Place your PDF documents in the `data/` folder:
- NEC code documents (filename should contain "nec" or "2017")
- Wattmonk information documents (filename should contain "wattmonk")

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure
```
wattmonk-rag-chatbot/
├── app.py                      # Main Streamlit application
├── src/
│   ├── document_processor.py  # PDF processing and chunking
│   ├── vector_store.py        # Document storage and retrieval
│   └── chatbot.py             # RAG logic and LLM integration
├── data/                       # Place your PDF documents here
├── docs/                       # Documentation files
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in Git)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 💡 Usage

### Starting a Conversation

Simply type your question in the chat input at the bottom of the page.

### Example Queries

**NEC Code Questions:**
```
What is the NEC code for grounding requirements?
What are the voltage requirements for residential circuits?
Tell me about conductor sizing requirements
```

**Wattmonk Information:**
```
What services does Wattmonk provide?
Tell me about Wattmonk's solar design capabilities
What is Wattmonk's contact information?
```

**General Questions:**
```
What is artificial intelligence?
Explain how solar panels work
What's the difference between AC and DC current?
```

### Using the Search Feature

1. Click on "🔍 Search Documents" to expand the search panel
2. Enter your search keywords
3. Click "Search" to find relevant passages across all documents
4. Results show the source document and page number

### Sidebar Features

- **System Info**: View document statistics
- **Example Queries**: Click to instantly try sample questions
- **Clear Chat History**: Reset the conversation

## 🔧 Configuration

### Adjusting Chunk Size

In `src/document_processor.py`, modify the `DocumentProcessor` initialization:
```python
processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
```

### Changing the LLM Model

In `src/chatbot.py`, update the model name:
```python
self.model = genai.GenerativeModel('gemini-2.5-flash')
```

Available models: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.0-flash`

### Customizing Intent Keywords

Edit the keyword lists in `src/chatbot.py` under the `classify_intent` method to improve classification accuracy.

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Add your `GOOGLE_API_KEY` in the Secrets section
5. Deploy!

### Other Platforms

- **Hugging Face Spaces**: Deploy as a Streamlit app
- **Railway**: Use the Streamlit template
- **Google Cloud Run**: Containerize and deploy
- **Heroku**: Use Streamlit buildpack

## 📊 Performance

- **Response Time**: 2-4 seconds per query
- **Document Processing**: ~30 seconds for initial load
- **Memory Usage**: ~200MB for moderate document sizes
- **Concurrent Users**: Scales with Streamlit Cloud tier

## 🔒 Security

- API keys stored in `.env` file (not committed to Git)
- Input sanitization for user queries
- No sensitive data logged
- HTTPS enforced on deployed version

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure `.env` file exists in the root directory
- Check that the API key is correctly formatted

### "No results found" for valid queries
- Verify PDF documents are in the `data/` folder
- Check that filenames contain "nec" or "wattmonk" for proper classification
- Try more specific keywords

### Slow response times
- Check your internet connection
- Consider using `gemini-2.5-flash` instead of `gemini-2.5-pro`
- Reduce chunk size for faster processing

## 📝 Future Enhancements

- [ ] Implement proper vector database (Pinecone/Weaviate)
- [ ] Add conversation memory persistence
- [ ] Multi-language support
- [ ] Confidence scoring for responses
- [ ] Query refinement suggestions
- [ ] Export chat history
- [ ] Advanced analytics dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Your Name**
- GitHub: [@Dhaka08](https://github.com/Dhaka08)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Wattmonk Technologies for the internship opportunity
- Google for Gemini API
- Streamlit for the amazing framework
- The open-source community

## 📞 Support

For questions or issues, please open an issue on GitHub or contact [himanshudhaka05@gmail.com](mailto:himanshudhaka05@gmail.com)

---

Built with ❤️ for Wattmonk Technologies Internship Assignment