# 📧 Email Productivity Agent

A production-ready, AI-powered email management system that helps you categorize emails, extract action items, generate draft replies, and interact with your inbox through an intelligent agent interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

### Phase 1: Email Categorization & Action Item Extraction
- ✅ Automatic email categorization (Important, To-Do, Newsletter, Spam)
- ✅ AI-powered action item extraction with deadlines and priorities
- ✅ Batch processing of multiple emails
- ✅ SQLite database for persistent storage
- ✅ Processing logs for debugging and auditing

### Phase 2: Configurable Prompts (Prompt Brain)
- ✅ Editable categorization prompts
- ✅ Customizable action extraction templates
- ✅ Draft generation prompt configuration
- ✅ Tone selection (Professional, Friendly, Casual)
- ✅ Reset to default prompts functionality
- ✅ Real-time prompt updates

### Phase 3: Intelligent Agent Chat
- ✅ Natural language queries about emails
- ✅ Context-aware conversations
- ✅ Single email queries ("Summarize this email")
- ✅ Inbox-wide queries ("Show urgent emails")
- ✅ Conversation history management
- ✅ Quick action buttons
- ✅ Draft reply generation
- ✅ Export conversation history

## 📸 Screenshots

*(Application interface with three-column layout: Inbox, Email Details, and Agent Chat)*

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  Backend Logic   │────▶│  OpenAI API     │
│   (app.py)      │     │  (Processors)    │     │  (GPT-4)        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        │                        │
        ▼                        ▼
┌─────────────────┐     ┌──────────────────┐
│  Components     │     │  SQLite Database │
│  (UI Modules)   │     │  (email_agent.db)│
└─────────────────┘     └──────────────────┘
```

### Tech Stack
- **Frontend**: Streamlit 1.30.0
- **AI/LLM**: OpenAI API (GPT-4 Turbo)
- **Database**: SQLite with SQLAlchemy
- **Language**: Python 3.11+
- **Deployment**: Heroku, Railway, or Render ready

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git (optional)

### Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/email-productivity-agent.git
cd email-productivity-agent
```

Or download and extract the ZIP file.

### Step 2: Set Up Environment

**On Windows:**
```cmd
setup.bat
```

**On Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Configure API Key

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
DATABASE_PATH=data/email_agent.db
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

### Step 4: Run the Application

```bash
# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Run Streamlit app
streamlit run ui/app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Loading Emails

On first launch, the app automatically loads 20 sample emails from `data/mock_inbox.json`. These emails represent a diverse inbox with:
- Meeting requests
- Task assignments
- Newsletters
- Security alerts
- Spam emails
- Project updates

### 2. Configuring Prompts

Click on the **🧠 Prompt Brain** sections in the sidebar to customize:

**Categorization Prompt:**
- Controls how emails are classified
- Defines category rules and criteria
- Temperature: 0.3 (more deterministic)

**Action Item Extraction:**
- Extracts tasks with deadlines and priorities
- Returns structured JSON format
- Temperature: 0.5

**Auto-Reply Draft:**
- Generates contextual replies
- Supports tone selection
- Temperature: 0.8 (more creative)

Click **💾 Save** to apply changes or **🔄 Reset** to restore defaults.

### 3. Processing Emails

**Single Email:**
1. Select an email from the inbox
2. Click **🔄 Process Email** in the detail view
3. Wait for AI categorization and action extraction

**Batch Processing:**
1. Filter emails (optional)
2. Click **🔄 Process All** above the inbox
3. Progress bar shows completion status

### 4. Using the Agent Chat

**Quick Actions:**
- 📝 **Summarize**: Get a concise summary of the selected email
- 📋 **Extract Tasks**: List all action items
- ✉️ **Draft Reply**: Generate a professional response
- 🚨 **Show Urgent**: Display Important and To-Do emails

**Natural Language Queries:**
```
"What are my tasks for this week?"
"Show me emails from sarah.johnson@techcorp.com"
"How many unread emails do I have?"
"Summarize the project deadline email"
"Draft a reply asking for more details"
```

**Conversation Features:**
- Context-aware responses
- Remembers last 5 messages
- Export chat history
- Clear conversation anytime

### 5. Managing Drafts

**Generate Draft:**
1. Select an email
2. Switch to **✉️ Drafts** view
3. Add custom instructions (optional)
4. Click **✨ Generate Draft**

**Edit Draft:**
- Modify subject and body directly
- Preview original email
- Download as text file
- Regenerate with different approach

**⚠️ Important**: Drafts are **NEVER sent automatically**. They are for review only.

## 🧪 Testing

Run the test suite:

```bash
# Activate virtual environment first
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_processor.py -v
pytest tests/test_agent.py -v
```

## 🚢 Deployment

### Deploy to Heroku

1. Install Heroku CLI
2. Create new app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your-key-here
```

4. Deploy:
```bash
git push heroku main
```

### Deploy to Railway

1. Connect GitHub repository
2. Add environment variables in dashboard
3. Railway auto-detects `Procfile` and deploys

### Deploy to Render

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run ui/app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables

## 📁 Project Structure

```
email-productivity-agent/
├── backend/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # SQLite operations
│   ├── models.py              # Data models
│   ├── llm_service.py         # OpenAI integration
│   ├── email_processor.py     # Email processing pipeline
│   └── agent_logic.py         # Agent reasoning
├── data/
│   ├── mock_inbox.json        # 20 sample emails
│   └── email_agent.db         # SQLite database (auto-created)
├── prompts/
│   └── default_prompts.json   # Default prompt templates
├── ui/
│   ├── app.py                 # Main Streamlit app
│   └── components/
│       ├── inbox_viewer.py    # Email list & detail
│       ├── prompt_editor.py   # Prompt configuration
│       ├── agent_chat.py      # Chat interface
│       └── draft_manager.py   # Draft management
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_processor.py      # Processor tests
│   └── test_agent.py          # Agent tests
├── .env.example               # Environment template
├── .gitignore
├── requirements.txt           # Python dependencies
├── setup.sh / setup.bat       # Setup scripts
├── Procfile                   # Heroku deployment
├── runtime.txt                # Python version
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | Model to use | `gpt-4-turbo-preview` |
| `DATABASE_PATH` | SQLite database location | `data/email_agent.db` |
| `MAX_RETRIES` | API retry attempts | `3` |
| `TIMEOUT_SECONDS` | API timeout | `30` |

### Model Options

- `gpt-4-turbo-preview` - Most capable (recommended)
- `gpt-4` - Reliable and accurate
- `gpt-3.5-turbo` - Faster and cheaper

## 💰 Cost Estimation

Based on OpenAI pricing (as of Nov 2025):

- **Initial load (20 emails)**: ~$0.20 - $0.40
- **Single email processing**: ~$0.01 - $0.02
- **Draft generation**: ~$0.02 - $0.04
- **Agent query**: ~$0.01 - $0.03

**Monthly estimate** (200 emails): ~$5 - $10

Use `gpt-3.5-turbo` for lower costs (~70% savings).

## 🐛 Troubleshooting

### "Configuration Error: OPENAI_API_KEY not set"
- Ensure `.env` file exists in project root
- Verify API key starts with `sk-`
- Restart the application

### "Database initialization failed"
- Check write permissions in `data/` folder
- Delete `data/email_agent.db` and restart
- Run `python -c "from backend.database import init_database; init_database()"`

### "No emails found"
- Verify `data/mock_inbox.json` exists
- Check JSON file is valid
- Look for errors in terminal output

### "LLM request failed"
- Verify internet connection
- Check API key is valid
- Check OpenAI service status
- Review rate limits on your account

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version is 3.11+

## 📊 Database Schema

### Tables

**emails**
- `id` (INTEGER, PRIMARY KEY)
- `sender` (TEXT)
- `subject` (TEXT)
- `body` (TEXT)
- `timestamp` (TEXT)
- `has_attachment` (INTEGER)
- `category` (TEXT)
- `action_items_json` (TEXT)
- `processed` (INTEGER)
- `created_at` (TEXT)

**prompts**
- `id` (INTEGER, PRIMARY KEY)
- `prompt_type` (TEXT, UNIQUE)
- `prompt_text` (TEXT)
- `is_active` (INTEGER)
- `created_at` (TEXT)
- `updated_at` (TEXT)

**drafts**
- `id` (INTEGER, PRIMARY KEY)
- `email_id` (INTEGER, FOREIGN KEY)
- `subject` (TEXT)
- `body` (TEXT)
- `metadata_json` (TEXT)
- `created_at` (TEXT)

**processing_logs**
- `id` (INTEGER, PRIMARY KEY)
- `email_id` (INTEGER, FOREIGN KEY)
- `operation` (TEXT)
- `status` (TEXT)
- `llm_response` (TEXT)
- `error_message` (TEXT)
- `timestamp` (TEXT)

## 🔐 Security & Privacy

- ✅ API keys stored in `.env` (never committed)
- ✅ Input sanitization and validation
- ✅ SQL injection prevention (parameterized queries)
- ✅ No auto-sending of emails (draft-only mode)
- ✅ Local database storage (SQLite)
- ⚠️ **Important**: Never share your `.env` file or API keys

## 🚀 Future Enhancements

- [ ] Email provider integration (Gmail, Outlook)
- [ ] Real-time email monitoring
- [ ] Multi-user support with authentication
- [ ] Email threading and conversation view
- [ ] Advanced analytics dashboard
- [ ] Calendar integration for deadlines
- [ ] Webhook support for automation
- [ ] Mobile-responsive design improvements
- [ ] Dark mode UI theme
- [ ] Export reports (PDF, CSV)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 Email Productivity Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

Built with ❤️ by the Email Productivity Agent Team

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Streamlit for the amazing framework
- The Python community

## 📞 Support

- 📧 Email: support@emailagent.example
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/email-productivity-agent/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/email-productivity-agent/discussions)

---

**⚠️ Disclaimer**: This is a demonstration project. Drafts are for review purposes only and are never sent automatically. Always review AI-generated content before using it in production.

**Made with Streamlit** 🎈 | **Powered by OpenAI** 🤖
