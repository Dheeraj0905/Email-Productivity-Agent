# 🎬 Demo Presentation Guide

## 📋 Pre-Demo Checklist

### Before You Start
- [ ] Ollama is running (if using local AI)
- [ ] `.env` file is configured
- [ ] Virtual environment is activated
- [ ] App is running at http://localhost:8501
- [ ] Browser window is ready
- [ ] Sample emails are loaded (20 emails)

### Quick Setup
```bash
cd "d:\Projects\Email Productivity Agent"
venv\Scripts\activate
streamlit run ui/app.py
```

---

## 🎯 Demo Flow (10-15 minutes)

### **1. Introduction (1 min)**
> "This is an AI-powered Email Productivity Agent that helps manage your inbox automatically."

**Show:**
- Landing page with 20 sample emails
- Clean, modern interface
- AI provider badge (Ollama/OpenAI)

---

### **2. Email Categorization (2 min)**
> "Watch how the AI automatically categorizes emails based on content."

**Steps:**
1. Select an unprocessed email (gray icon 📩)
2. Click **"⚡ Process Email"**
3. Wait for AI to analyze
4. Show the result:
   - Category assigned (Important/To-Do/Newsletter/Spam)
   - Color-coded badge

**Sample emails to demo:**
- "Q4 Project Deadline" → Should be **To-Do**
- "URGENT: Security Patch" → Should be **Important**
- "Weekly Tech News" → Should be **Newsletter**
- "You've Won $5,000,000!" → Should be **Spam**

---

### **3. Action Item Extraction (2 min)**
> "The AI can extract actionable tasks with deadlines and priorities."

**Steps:**
1. Select a meeting/task email
2. Process it (if not done)
3. Scroll to **"✅ Action Items"**
4. Show extracted tasks with:
   - Task description
   - Deadline (if any)
   - Priority (High/Medium/Low with colored icons)

**Best demo emails:**
- "Design Review Meeting - Agenda Needed"
- "Annual Performance Review Scheduled"
- "[Repository] New Pull Request"

---

### **4. Batch Processing (1 min)**
> "Process multiple emails at once for efficiency."

**Steps:**
1. Click **"Process All"** button
2. Show progress bar
3. Display success message: "✓ Batch processing complete: X/20 successful"
4. Show inbox with all processed emails (✅ icons)

---

### **5. AI Chat Assistant (3 min)**
> "Ask questions about your inbox in natural language."

**Demo queries:**
```
1. "Show me urgent emails"
   → Agent filters and lists Important/To-Do emails

2. "What are my deadlines this week?"
   → Agent extracts tasks with deadlines

3. "Summarize the security patch email"
   → Agent provides concise summary

4. "Show me emails from Sarah"
   → Agent filters by sender
```

**Show:**
- Natural conversation flow
- Context-aware responses
- Quick action buttons (Summarize, Extract Tasks, Draft Reply)

---

### **6. Draft Generation (2 min)**
> "Generate professional reply drafts with custom tone."

**Steps:**
1. Select an email (e.g., meeting invite)
2. Switch to **"Drafts"** view
3. Click **"✨ Generate Draft"**
4. Show generated reply
5. Demo tone selector:
   - Professional
   - Friendly
   - Casual
6. Emphasize: **"Drafts are NEVER sent automatically"**

---

### **7. Prompt Brain Customization (2 min)**
> "Customize how the AI thinks and responds."

**Steps:**
1. Expand **"🧠 Prompt Brain"** in sidebar
2. Show categorization prompt
3. Explain temperature control:
   - Low (0.3) = More deterministic
   - High (0.8) = More creative
4. Demo quick reset: **"🔄 Reset to Default"**
5. Show save functionality

---

### **8. Dashboard & Analytics (1 min)**
> "Monitor your email productivity at a glance."

**Show sidebar:**
- Total emails: 20
- Done: X
- Pending: Y
- Progress: X%
- API Calls counter (if using OpenAI)

**Highlight:**
- Real-time stats
- Processing rate percentage
- Model information

---

### **9. Filtering & Search (1 min)**
> "Find exactly what you need quickly."

**Demo:**
1. Click **"Filters"** expander
2. Filter by Category dropdown
3. Filter by Status (Processed/Unprocessed)
4. Use search bar to find specific email
5. Sort by Date/Sender/Category

---

### **10. Closing (1 min)**
> "Key takeaways and technical highlights."

**Emphasize:**
- ✅ Dual AI support (OpenAI & Ollama)
- ✅ Configurable prompts
- ✅ Natural language queries
- ✅ Batch processing
- ✅ Privacy-first (drafts never auto-sent)
- ✅ Production-ready architecture

**Tech Stack:**
- Frontend: Streamlit
- AI: GPT-4 / Llama 3.2
- Database: SQLite
- Backend: Python

---

## 💡 Pro Tips for Demo

### Do's ✅
- Start with fresh database (delete `data/email_agent.db`)
- Process 2-3 emails before showing chat
- Use diverse sample emails for categorization
- Keep queries simple and clear
- Show error handling (optional)

### Don'ts ❌
- Don't wait for slow API responses (use Ollama for speed)
- Don't process all emails at start (save for batch demo)
- Don't skip the "drafts never auto-send" disclaimer
- Don't use technical jargon with non-tech audience

---

## 🎯 Audience-Specific Angles

### For Technical Audience
- Emphasize architecture (unified LLM service)
- Show code structure briefly
- Discuss prompt engineering
- Mention SQLite schema
- Talk about extensibility

### For Business Audience
- Focus on time savings
- Show ROI potential
- Emphasize ease of use
- Discuss cost (OpenAI vs Ollama)
- Highlight automation benefits

### For Product Managers
- Feature roadmap potential
- Integration possibilities (Gmail, Outlook)
- Scalability discussion
- User experience focus
- Customization capabilities

---

## 🚨 Troubleshooting During Demo

### If OpenAI is slow:
- Switch to Ollama (faster locally)
- Reduce temperature
- Use GPT-3.5 instead of GPT-4

### If app crashes:
- Restart Streamlit: `streamlit run ui/app.py`
- Check `.env` configuration
- Verify Ollama is running

### If no emails show:
- Check `data/mock_inbox.json` exists
- Reload browser
- Restart app

### If chat doesn't respond:
- Check API key / Ollama connection
- Look at terminal for errors
- Verify email is processed first

---

## ⏱️ Quick Demo (5 min version)

For time-constrained presentations:

1. **Show interface** (30 sec)
2. **Process one email** → show category + actions (1 min)
3. **Batch process all** (30 sec)
4. **Chat query**: "Show urgent emails" (1 min)
5. **Generate draft reply** (1 min)
6. **Show prompt customization** (1 min)

---

## 🎬 Demo Script Template

> "Good [morning/afternoon]! Today I'm presenting an AI-powered Email Productivity Agent.
>
> Imagine spending hours sorting emails, extracting tasks, and drafting replies. This tool automates all of that using AI.
>
> [Process an email]
> As you can see, it automatically categorized this as 'Important' and extracted 3 action items with priorities.
>
> [Show batch processing]
> Now let's process the entire inbox in seconds.
>
> [Use chat]
> The real magic is the AI assistant. I can ask 'Show me urgent emails' and it intelligently filters them.
>
> [Generate draft]
> Need to reply? It can generate a professional draft in any tone.
>
> [Show customization]
> And everything is customizable through the Prompt Brain.
>
> This runs on either OpenAI's GPT-4 or locally with Ollama for zero API costs.
>
> Questions?"

---

## 📊 Expected Demo Metrics

After full demo run:
- **Emails processed**: 20/20
- **Categories assigned**: 100%
- **Action items extracted**: ~25-30
- **Chat queries**: 5-7
- **Drafts generated**: 1-2
- **Time taken**: 10-15 minutes
- **OpenAI cost**: ~$0.50-1.00
- **Ollama cost**: $0 (free)

---

**Ready to Present!** 🚀
