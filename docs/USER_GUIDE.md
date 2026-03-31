# 📖 User Guide - Wattmonk RAG Chatbot

Welcome to the Wattmonk AI Assistant! This guide will help you get the most out of the chatbot.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Using the Chatbot](#using-the-chatbot)
3. [Search Feature](#search-feature)
4. [Understanding Responses](#understanding-responses)
5. [Tips for Better Results](#tips-for-better-results)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Time Setup

1. **Access the Application**
   - Local: Open your browser to `http://localhost:8501`
   - Deployed: Visit the provided Streamlit Cloud URL

2. **Wait for Initialization**
   - The app will load and process documents (takes ~30 seconds)
   - You'll see "Loading documents..." and "Building vector database..." messages
   - Once complete, the chat interface appears

3. **Interface Overview**
```
   ┌─────────────────────────────────────────────────┐
   │  ⚡ Wattmonk AI Assistant                       │
   ├─────────────────────────────────────────────────┤
   │                                                  │
   │  [Chat messages appear here]                    │
   │                                                  │
   ├─────────────────────────────────────────────────┤
   │  Ask me anything... [Input Box]          [Send] │
   └─────────────────────────────────────────────────┘
```

---

## Using the Chatbot

### Asking Questions

Simply type your question in the input box at the bottom and press Enter or click Send.

### Types of Questions

#### 1. NEC Code Questions

**What to ask:**
- Electrical code requirements
- Wiring standards
- Circuit specifications
- Installation regulations
- Grounding requirements
- Voltage specifications

**Example Questions:**
```
✓ What is the NEC code for grounding requirements?
✓ What are the voltage requirements for residential wiring?
✓ Tell me about circuit breaker specifications
✓ What does NEC say about conductor sizing?
✓ Explain ampacity requirements for cables
```

**Keywords that trigger NEC search:**
- "NEC", "electrical code", "wiring", "circuit"
- "voltage", "ampere", "grounding", "conductor"
- "panel", "breaker", "installation", "regulation"

#### 2. Wattmonk Company Questions

**What to ask:**
- Company services
- Solar design capabilities
- Team information
- Contact details
- Pricing information

**Example Questions:**
```
✓ What services does Wattmonk provide?
✓ Tell me about Wattmonk's solar design services
✓ How can I contact Wattmonk?
✓ What is Wattmonk's expertise?
✓ Does Wattmonk offer engineering services?
```

**Keywords that trigger Wattmonk search:**
- "Wattmonk", "company", "service", "team"
- "solar", "design", "pricing", "contact"

#### 3. General Knowledge Questions

**What to ask:**
- General electrical concepts
- Solar technology basics
- Physics principles
- Definitions
- Explanations not specific to NEC or Wattmonk

**Example Questions:**
```
✓ What is artificial intelligence?
✓ Explain how solar panels work
✓ What's the difference between AC and DC current?
✓ How do batteries store energy?
✓ What is renewable energy?
```

---

## Search Feature

### Using Document Search

1. **Open Search Panel**
   - Click on "🔍 Search Documents" expander
   - The search panel will open below the header

2. **Enter Search Terms**
   - Type specific keywords you want to find
   - Be specific (e.g., "grounding electrode" vs just "ground")

3. **View Results**
   - Results show:
     - Document source (NEC Code or Wattmonk Information)
     - Page number
     - Text snippet (first 300 characters)
   - Up to 5 results displayed

4. **Example Searches**
```
   ✓ "grounding electrode conductor"
   ✓ "solar panel installation"
   ✓ "circuit breaker sizing"
   ✓ "residential wiring"
```

### When to Use Search vs Chat

**Use Search when:**
- You want to browse document content
- Looking for specific technical terms
- Need to see multiple relevant passages
- Want to verify information location

**Use Chat when:**
- You want a direct answer
- Need explanations or summaries
- Asking comparative questions
- Having a conversation

---

## Understanding Responses

### Response Components

Each chatbot response includes:

1. **Answer Text**
   - The main response to your question
   - Written in clear, professional language

2. **Source Badge**
   - Shows where the information came from
   - Color-coded by source type:
     - 🟡 Yellow: NEC Code
     - 🔵 Blue: Wattmonk Information
     - 🟢 Green: Base Knowledge (general AI knowledge)

3. **Page Numbers** (for document-based answers)
   - Shows specific pages referenced
   - Format: "Page 42" or "Pages 42, 45, 67"
   - Helps you verify or read more in original documents

### Example Response Breakdown
```
┌────────────────────────────────────────────────┐
│ Q: What is the NEC grounding requirement?      │
├────────────────────────────────────────────────┤
│ A: According to the NEC code, grounding        │ ← Answer
│    electrodes must be installed to provide     │
│    a direct connection to earth...             │
│                                                 │
│ 📚 Source: NEC Code | Pages 42, 45            │ ← Source + Pages
└────────────────────────────────────────────────┘
```

### Response Quality Indicators

**High-Confidence Response:**
- Specific details and references
- Multiple page citations
- Direct quotes or paraphrases from documents

**Medium-Confidence Response:**
- General information from documents
- Fewer citations
- May combine multiple sources

**Fallback Response:**
- "I couldn't find specific information in the documents..."
- Suggestions for related questions
- Offers to help with alternatives

---

## Tips for Better Results

### Writing Effective Questions

#### ✅ DO:
- **Be specific**: "What is the minimum wire gauge for 20A circuits?" instead of "Tell me about wires"
- **Use technical terms**: "grounding electrode" is better than "ground thing"
- **Ask one question at a time**: Break complex queries into parts
- **Include context**: "For residential installations, what is..." helps classification

#### ❌ DON'T:
- Ask vague questions: "Tell me everything about NEC"
- Use overly casual language: "What's that wire thingy called?"
- Combine multiple unrelated questions in one query
- Expect information not in the loaded documents

### Getting Specific Information

**Instead of:**
```
❌ "Tell me about Wattmonk"
```

**Try:**
```
✓ "What services does Wattmonk offer?"
✓ "What is Wattmonk's expertise in solar design?"
✓ "How can I contact Wattmonk for a project?"
```

### Following Up

You can ask follow-up questions naturally:
```
1. "What is the NEC requirement for grounding?"
2. "Can you explain that in simpler terms?"
3. "What are the exceptions to this rule?"
```

---

## Sidebar Features

### System Information
- **NEC Code Chunks**: Number of text segments from NEC documents
- **Wattmonk Info Chunks**: Number of text segments from Wattmonk documents
- Higher numbers = more comprehensive coverage

### Capabilities List
Shows what the chatbot can do - use this as a quick reference

### Example Queries
Click any example button to instantly try that question

### Clear Chat History
- Resets the conversation
- Useful for starting fresh
- Doesn't affect loaded documents

---

## Troubleshooting

### Common Issues

#### "No specific context found"

**Problem**: The chatbot couldn't find relevant information in the documents.

**Solutions**:
- Try different keywords
- Rephrase your question
- Use the Search feature to browse available content
- Ask more general questions that use base knowledge

#### Slow Responses

**Problem**: The chatbot takes a long time to respond.

**Causes**:
- Large documents being processed
- Internet connection speed
- API rate limits

**Solutions**:
- Wait patiently for first response (API call)
- Check your internet connection
- Try again if it times out

#### Incorrect Source Classification

**Problem**: A question about NEC gets marked as "General" or vice versa.

**Why**: The intent classifier uses keywords that might not match your phrasing.

**Solutions**:
- Include specific keywords (like "NEC" or "Wattmonk")
- Rephrase to use technical terms
- Use the Search feature for precise document lookup

#### Generic or Unhelpful Answers

**Problem**: Response doesn't answer your specific question.

**Solutions**:
- Be more specific in your question
- Break complex questions into parts
- Ask for specific aspects (e.g., "What's the voltage?" vs "Tell me about it")
- Check if the information exists using Search

---

## Advanced Usage

### Comparing Information

You can ask comparative questions:
```
✓ "What's the difference between grounding and bonding in NEC?"
✓ "Compare Wattmonk's services to typical solar companies"
```

### Multi-Step Questions

Break complex queries into steps:
```
1. "What are the NEC requirements for outdoor wiring?"
2. "What wire types meet those requirements?"
3. "How should they be installed?"
```

### Verification

Use page numbers to verify information:
1. Ask a question
2. Note the page numbers in the response
3. Check those pages in the original PDF for full context

---

## Best Practices

### For Technical Research
1. Start with broad questions
2. Drill down into specific requirements
3. Use Search to browse related content
4. Note page numbers for reference

### For Quick Answers
1. Use example queries as templates
2. Be direct and specific
3. Trust the source attribution
4. Ask follow-ups if needed

### For Learning
1. Ask "What is..." style questions
2. Request explanations or examples
3. Ask for comparisons
4. Use general knowledge mode for concepts

---

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Ctrl/Cmd + K**: Focus on search input (when in search panel)

---

## Privacy & Data

- Your questions are sent to Google Gemini API for processing
- No conversation history is permanently stored
- No personal data is collected
- Documents are processed locally
- Clearing chat removes all conversation data from session

---

## Getting Help

### If You're Stuck:
1. Try the example queries
2. Use the Search feature to explore available content
3. Ask simpler, more specific questions
4. Check this guide for tips

### If Something's Broken:
1. Refresh the page
2. Clear chat history with the sidebar button
3. Check that documents are loaded (see sidebar stats)
4. Report issues to the repository

---

## FAQ

**Q: Can I upload my own documents?**  
A: Not through the UI, but you can add PDFs to the `data/` folder and restart the app.

**Q: Does it remember previous conversations?**  
A: Within a session, yes. But it's cleared when you refresh or restart.

**Q: How accurate are the responses?**  
A: Responses based on documents are highly accurate. General knowledge depends on the AI model.

**Q: Can I use this offline?**  
A: No, it requires an internet connection for the Google Gemini API.

**Q: What if the answer references the wrong page?**  
A: Page numbers come from PDF extraction and should be accurate, but verify in the source document.

**Q: Can I export the chat?**  
A: Not currently, but you can copy-paste the conversation.

---

## Feedback

We'd love to hear your feedback!
- Report bugs or issues on GitHub
- Suggest features or improvements
- Share your experience

---

**Happy chatting! 🎉**

For more technical information, see [ARCHITECTURE.md](ARCHITECTURE.md)