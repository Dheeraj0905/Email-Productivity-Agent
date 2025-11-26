# Email Productivity Agent - Demo

An AI-powered email management system that helps you categorize emails, extract action items, and interact with your inbox through an intelligent chat interface.

## Key Features

- **Smart Categorization** - Automatically sorts emails (Important, To-Do, Newsletter, Spam)
- **Action Items** - Extracts tasks with deadlines and priorities
- **AI Chat Assistant** - Ask questions about your emails in natural language
- **Draft Generation** - Auto-generate reply drafts with custom tone
- **Configurable Prompts** - Customize AI behavior through the Prompt Brain
- **Batch Processing** - Process multiple emails at once
- **Dual AI Support** - Works with OpenAI or Ollama (local, free)

## Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key OR Ollama installed locally

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Email-Productivity-Agent.git
cd Email-Productivity-Agent
```

2. **Set up virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**

Create a `.env` file:
```env
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# OR for Ollama (free, local)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

5. **Run the app**
```bash
streamlit run ui/app.py
```

The app will open at `http://localhost:8501`

## 📖 Demo Usage

### 1. Loading Sample Emails
The app automatically loads 20 sample emails on first launch from `data/mock_inbox.json`

### 2. Processing Emails
- **Single Email**: Select an email → Click "⚡ Process Email"
- **Batch**: Click "Process All" to process multiple emails

### 3. Using the AI Chat
Quick actions:
- **📝 Summarize** - Get email summary
- **📋 Extract Tasks** - List action items
- **✉️ Draft Reply** - Generate response
- **🚨 Show Urgent** - Filter important emails

Natural language queries:
```
"Show me emails from John"
"What are my deadlines this week?"
"Summarize the project update email"
```

### 4. Customizing Prompts
Click "🧠 Prompt Brain" in sidebar to:
- Edit categorization rules
- Modify action extraction format
- Change reply generation style
- Adjust AI temperature

## 🔧 Configuration

### AI Providers

**OpenAI** (Cloud - Paid)
- Most capable and reliable
- Models: GPT-4, GPT-3.5 Turbo
- Setup: Add API key to `.env`

**Ollama** (Local - Free)
- No API costs
- Works offline
- Setup guide: See `OLLAMA_SETUP.md`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | AI provider (`openai` or `ollama`) | `openai` |
| `OPENAI_API_KEY` | Your OpenAI API key | Required for OpenAI |
| `OPENAI_MODEL` | Model to use | `gpt-4-turbo-preview` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |

## 📁 Project Structure

```
Email-Productivity-Agent/
├── backend/                 # Core logic
│   ├── config.py           # Configuration
│   ├── database.py         # SQLite operations
│   ├── models.py           # Data models
│   ├── llm_service.py      # OpenAI integration
│   ├── ollama_service.py   # Ollama integration
│   ├── unified_llm_service.py  # AI abstraction
│   ├── email_processor.py  # Email processing
│   └── agent_logic.py      # Agent reasoning
│
├── ui/                     # Streamlit interface
│   ├── app.py              # Main app
│   └── components/         # UI components
│
├── data/                   # Data files
│   └── mock_inbox.json     # Sample emails
│
├── prompts/                # AI prompts
│   └── default_prompts.json
│
├── .env                    # Your config (not in git)
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 💡 Demo Tips

### For Best Demo Experience:
1. **Use OpenAI** for most reliable results (GPT-4)
2. **Process a few emails** before showing chat
3. **Demo quick actions** for visual impact
4. **Show prompt customization** to highlight flexibility
5. **Try natural language queries** to show intelligence

### Common Demo Scenarios:
- **Scenario 1**: Show auto-categorization accuracy
- **Scenario 2**: Extract action items from meeting invite
- **Scenario 3**: Generate professional reply draft
- **Scenario 4**: Chat to find urgent emails
- **Scenario 5**: Batch process entire inbox

## 🐛 Troubleshooting

### "Configuration Error"
- Check `.env` file exists
- Verify API key is correct (starts with `sk-`)
- Ensure `LLM_PROVIDER` is set

### "No emails found"
- Verify `data/mock_inbox.json` exists
- Reload the page

### "Ollama connection failed"
- Make sure Ollama is running
- Check OLLAMA_BASE_URL in `.env`
- See `OLLAMA_SETUP.md` for help

### "API rate limit"
- You've hit OpenAI usage limits
- Wait a few minutes or upgrade plan
- Switch to Ollama for free alternative

## 💰 Cost Note

**OpenAI Costs** (Demo usage):
- Processing 20 emails: ~$0.20-0.50
- 10-20 chat queries: ~$0.10-0.30
- Total demo session: ~$0.50-1.00

**Ollama**: Completely free, runs locally

## 🔐 Security

- ✅ API keys stored in `.env` (not committed)
- ✅ `.env` is in `.gitignore`
- ✅ Drafts are NEVER sent automatically
- ⚠️ **Never share your `.env` file**

## 🎯 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **AI**: OpenAI GPT-4 / Ollama Llama 3.2
- **Database**: SQLite
- **Libraries**: SQLAlchemy, Pydantic, OpenAI SDK

---

**Built for Demo** | **AI-Powered** | **Production-Ready**
