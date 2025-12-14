# Email Productivity Agent

An intelligent email assistant that uses AI to help you manage your inbox more efficiently. Think of it as a smart assistant that reads your emails, understands what's important, and helps you take action.

## What Does It Do?

This application solves a common problem: **email overload**. Instead of manually sorting through hundreds of emails, the AI automatically:

1. **Categorizes your emails** into Important, To-Do, Newsletter, or Spam
2. **Finds action items** like deadlines, meetings, and tasks you need to complete
3. **Generates smart replies** so you can respond faster
4. **Answers questions** about your emails in plain English

### Real-World Example

**Before**: You have 50 unread emails. You spend 30 minutes reading through them to find urgent tasks.

**After**: The AI processes all 50 emails in seconds, highlights the 3 urgent ones, extracts 5 action items with deadlines, and lets you ask "What meetings do I have this week?"

## Key Features Explained

### 🎯 Smart Email Categorization
The AI reads each email and automatically labels it:
- **Important** 🔴 - Urgent emails requiring immediate attention
- **To-Do** 🟠 - Emails with tasks or action items
- **Newsletter** 🔵 - Promotional or informational content
- **Spam** ⚫ - Unwanted or irrelevant emails

### ✅ Action Item Extraction
The AI scans your emails and pulls out:
- Tasks you need to complete
- Deadlines and due dates
- Meeting invitations and calendar events
- Priority levels for each action

**Example**: From "Hi, please review the Q4 report by Friday EOD", it extracts:
- Task: "Review Q4 report"
- Deadline: "Friday 5:00 PM"
- Priority: High

### 💬 Conversational AI Assistant
Ask questions about your emails in natural language:
- "Show me emails from my manager"
- "What tasks are due this week?"
- "Summarize the project update email"
- "Do I have any meetings tomorrow?"

### ✍️ Smart Reply Generation
The AI drafts professional email responses for you:
- You select an email
- Choose a tone (professional, casual, brief)
- AI generates a complete draft
- You review, edit, and send

### 🧠 Customizable AI Behavior
You control how the AI thinks through the "Prompt Brain":
- Define what makes an email "Important"
- Teach it to recognize specific types of action items
- Set the tone and style for generated replies
- Adjust AI creativity vs. accuracy

## How It Works (Under the Hood)

```
1. You connect your emails → App loads them into the system
2. Click "Process" → AI reads and analyzes each email
3. AI uses language models → Understands context and intent
4. Results appear → Categories, tasks, and insights
5. You interact → Chat, generate replies, manage inbox
```

### The AI Brain

This app can work with two types of AI:

**Option 1: OpenAI (GPT-4)** - Cloud-based, most powerful
- Like having ChatGPT read your emails
- Very accurate and smart
- Costs ~$0.50-1.00 for a demo session

**Option 2: Ollama (Llama 3.2)** - Runs on your computer
- Completely free and private
- Works offline
- Good accuracy for most tasks

## Quick Start Guide

### What You Need
- A computer with Python installed
- Either an OpenAI API key ($20 credit) OR Ollama installed (free)
- 10 minutes to set up

### Setup in 5 Steps

**Step 1: Download the code**
```bash
git clone https://github.com/yourusername/Email-Productivity-Agent.git
cd Email-Productivity-Agent
```

**Step 2: Create an isolated environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**Step 3: Install required packages**
```bash
pip install -r requirements.txt
```

**Step 4: Configure your AI provider**

Create a file named `.env` and choose one:

```env
# Option A: Use OpenAI (more powerful, costs money)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Option B: Use Ollama (free, runs locally)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Step 5: Launch the app**
```bash
streamlit run ui/app.py
```

Opens automatically at `http://localhost:8501` 🎉
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

## Using the App - Step by Step

### First Launch
When you open the app, it automatically loads 20 sample emails so you can try it immediately. These are realistic work emails with various scenarios.

### Processing Emails

**Single Email Mode:**
1. Click on any email in the inbox list
2. Read it in the detail panel
3. Click "⚡ Process Email" button
4. Watch as the AI analyzes it (takes 2-5 seconds)
5. See the category badge and action items appear

**Batch Processing:**
1. Click "Process All Emails" button
2. AI processes all unread emails at once
3. Progress bar shows status
4. Results appear automatically

### Using the Chat Assistant

**Quick Actions** (one-click buttons):
- 📝 **Summarize Inbox** - Get overview of all emails
- 📋 **Extract All Tasks** - List every action item
- ✉️ **Draft Reply** - Generate response to selected email
- 🚨 **Show Urgent Emails** - Filter high-priority items

**Natural Conversation** (type anything):
```
You: "Show me emails about the marketing campaign"
AI: "Found 3 emails about marketing campaign:
     1. Budget approval request from Sarah
     2. Campaign timeline from John
     3. Design mockups from creative team"

You: "What's due this week?"
AI: "You have 4 tasks due this week:
     1. Approve marketing budget (Wednesday)
     2. Review design mockups (Thursday)
     3. Submit quarterly report (Friday)
     4. Schedule team meeting (Friday)"
```

### Generating Replies

1. Select an email you want to respond to
2. Click "✉️ Draft Reply" in chat
3. AI analyzes the email context
4. Generates a complete professional response
5. You review, edit if needed, then copy to send

**Example:**
- **Original**: "Can you send me the Q3 report by tomorrow?"
- **AI Draft**: "Hi [Name], I'll send over the Q3 report by end of day tomorrow. Please let me know if you need it in any specific format. Best regards, [Your Name]"

### Customizing AI Behavior

Click "🧠 Prompt Brain" in the sidebar to access the AI's instructions:

**Categorization Rules:**
Edit what the AI considers "Important" vs "Newsletter"
```
Example: "Mark emails with 'URGENT' in subject as Important"
```

**Action Item Format:**
Define how tasks should be extracted
```
Example: "Extract dates in format: MM/DD/YYYY"
```

**Reply Style:**
Set the tone for generated responses
```
Example: "Write replies in a friendly but professional tone"
```

## Project Architecture (For Technical Users)

### File Structure Explained
```
Email-Productivity-Agent/
├── backend/                    # The "brain" - All the logic
│   ├── config.py              # Settings and configuration
│   ├── database.py            # Saves emails to SQLite database
│   ├── models.py              # Defines data structure (email, task, etc.)
│   ├── llm_service.py         # Talks to OpenAI
│   ├── ollama_service.py      # Talks to Ollama
│   ├── unified_llm_service.py # Smart layer that switches between AIs
│   ├── email_processor.py     # Processes emails with AI
│   └── agent_logic.py         # Handles chat conversations
│
├── ui/                        # The "face" - What you see
│   ├── app.py                 # Main application interface
│   └── components/            # Reusable UI pieces
│       ├── inbox_viewer.py    # Email list display
│       ├── email_detail.py    # Single email view
│       ├── chat_interface.py  # Chat with AI
│       └── prompt_editor.py   # Customize AI behavior
│
├── data/                      # Storage
│   ├── email_agent.db         # SQLite database (created automatically)
│   └── mock_inbox.json        # Sample emails for demo
│
├── prompts/                   # AI instructions
│   └── default_prompts.json   # How AI should think
│
├── .env                       # YOUR configuration (never share!)
├── requirements.txt           # List of needed Python packages
└── README.md                  # This file
```

### How the AI Processing Works

```
Email arrives
    ↓
1. Email Processor receives it
    ↓
2. Unified LLM Service picks the right AI (OpenAI or Ollama)
    ↓
3. Categorization Prompt is sent to AI
    ↓
4. AI responds with category + confidence
    ↓
5. Action Item Extraction Prompt is sent
    ↓
6. AI extracts tasks, deadlines, priorities
    ↓
7. Results saved to Database
    ↓
8. UI updates to show results
```

### Technology Stack (What It's Built With)

- **Frontend**: Streamlit (Python web framework for data apps)
- **Backend**: Python 3.11+ (core programming language)
- **AI**: OpenAI GPT-4 or Ollama Llama 3.2 (language models)
- **Database**: SQLite (lightweight file-based database)
- **Data Handling**: SQLAlchemy (database toolkit), Pydantic (data validation)

## Demo Scenarios (For Presentations)

### Scenario 1: Email Overload
**Setup**: Show inbox with 20 unread emails
**Action**: Click "Process All"
**Result**: All emails categorized in 10 seconds, 8 action items extracted
**Takeaway**: "Saves 20+ minutes of manual sorting"

### Scenario 2: Finding Urgent Items
**Setup**: Processed inbox with mixed priority emails
**Action**: Click "🚨 Show Urgent Emails"
**Result**: Instantly filters to 3 high-priority emails
**Takeaway**: "Never miss important deadlines"

### Scenario 3: Smart Reply
**Setup**: Open a meeting invitation email
**Action**: Click "✉️ Draft Reply", review AI-generated response
**Result**: Professional acceptance email ready in 3 seconds
**Takeaway**: "Respond faster without sacrificing quality"

### Scenario 4: Natural Language Search
**Setup**: Chat interface with processed emails
**Action**: Type "What tasks are due this week?"
**Result**: AI lists all deadlines with dates
**Takeaway**: "Ask questions like talking to an assistant"

### Scenario 5: Custom AI Behavior
**Setup**: Open Prompt Brain
**Action**: Edit categorization rules to prioritize emails from specific people
**Result**: AI learns your preferences
**Takeaway**: "Fully customizable to your workflow"

## Troubleshooting Common Issues

### ❌ "Configuration Error: Ollama not running"
**Problem**: The app can't connect to Ollama
**Solution**: 
1. Open terminal
2. Run `ollama serve`
3. Refresh the app

### ❌ "Invalid API Key"
**Problem**: OpenAI key is wrong or expired
**Solution**:
1. Check `.env` file
2. Verify key starts with `sk-`
3. Get new key from platform.openai.com

### ❌ "No emails found"
**Problem**: Sample emails didn't load
**Solution**:
1. Check if `data/mock_inbox.json` exists
2. Click "Load Sample Data" in sidebar
3. Refresh the browser

### ❌ Processing is slow
**Problem**: AI responses taking 10+ seconds
**Possible causes**:
- Using Ollama on slow computer → Switch to OpenAI
- Poor internet connection → Check network
- Complex prompts → Simplify in Prompt Brain

### ❌ "Rate limit exceeded"
**Problem**: Too many OpenAI requests
**Solution**:
- Wait 1 minute between batch processing
- Upgrade OpenAI plan
- Switch to Ollama (no limits)

## Cost Information

### OpenAI Pricing (As of 2024)
- **GPT-4**: $0.03 per 1K input tokens, $0.06 per 1K output tokens
- **GPT-3.5**: $0.0015 per 1K input tokens, $0.002 per 1K output tokens

**Real costs for demo:**
- Processing 20 emails: $0.20-0.50
- 20 chat queries: $0.10-0.30
- Generating 10 replies: $0.15-0.25
- **Total demo session**: ~$0.50-1.00

**Tips to minimize cost:**
- Use GPT-3.5 instead of GPT-4 (10x cheaper, still good)
- Process emails in batches
- Set shorter prompt lengths

### Ollama (Free Forever)
- $0.00 per request
- Runs entirely on your computer
- Privacy bonus: emails never leave your machine
- Trade-off: Slightly less accurate than GPT-4

## Security & Privacy

### What's Safe ✅
- API keys stored locally in `.env` (not uploaded to Git)
- `.env` is in `.gitignore` (automatically excluded)
- Draft emails are NEVER sent automatically
- You always review before sending

### What to NEVER Do ❌
- Don't commit `.env` to GitHub
- Don't share your OpenAI API key
- Don't use on public/shared computers without logging out
- Don't process real sensitive emails in demos

### Privacy Options
**Most Private**: Use Ollama - emails stay on your computer
**Cloud Option**: OpenAI - emails sent to their servers for processing

## Future Enhancements (Roadmap)

Potential features for production version:
- [ ] Real email integration (Gmail, Outlook)
- [ ] Calendar integration (auto-add meetings)
- [ ] Email templates library
- [ ] Team collaboration features
- [ ] Mobile app interface
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Voice command interface

## Contributing

Found a bug? Have an idea?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - Feel free to use this project for learning, demos, or building upon it.

---

## Quick Reference Card

| Want to... | Do this... |
|------------|-----------|
| Process one email | Select email → Click "⚡ Process Email" |
| Process all emails | Click "Process All Emails" button |
| Find urgent emails | Click "🚨 Show Urgent Emails" |
| Get email summary | Click "📝 Summarize Inbox" |
| Generate reply | Select email → Click "✉️ Draft Reply" |
| Ask about emails | Type question in chat box |
| Customize AI | Click "🧠 Prompt Brain" |
| Switch AI provider | Edit `LLM_PROVIDER` in `.env` |

---

**Questions?** Open an issue on GitHub or contact dheerajkosuridk05@gmail.com

**Demo Ready** | **Production Quality** | **Open Source**
