# Ollama Setup Guide - FREE Local AI

## What is Ollama?
Ollama allows you to run large language models (like Llama 3.2) locally on your computer - **completely FREE**, with **no API costs**, and **no billing required**!

## ✅ Step-by-Step Setup

### Step 1: Install Ollama (2 minutes)

**Windows:**
1. Go to: https://ollama.com/download/windows
2. Download `OllamaSetup.exe`
3. Run the installer
4. That's it! Ollama is now installed

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Start Ollama (Automatic on Windows)

Ollama should start automatically after installation. If not:

```cmd
ollama serve
```

You should see: `Ollama is running`

### Step 3: Download the AI Model (5-10 minutes)

Open a **new terminal** and run:

```cmd
ollama pull llama3.2
```

This downloads the Llama 3.2 model (~2GB). You only need to do this once!

**Alternative models** (if llama3.2 doesn't work):
```cmd
ollama pull llama2       # Smaller, faster
ollama pull mistral      # Great quality
ollama pull phi          # Tiny, very fast
```

### Step 4: Test It Works

```cmd
ollama run llama3.2
```

Type a message to chat with the AI. Press `Ctrl+D` or type `/bye` to exit.

### Step 5: Install Python Package

```cmd
cd "d:\Projects\Email Productivity Agent"
venv\Scripts\activate
pip install requests
```

### Step 6: Run the App!

```cmd
streamlit run ui/app.py
```

## 🎯 That's It!

Your app now uses **FREE local AI** with:
- ✅ No API costs
- ✅ No billing required
- ✅ Works offline (after model download)
- ✅ Privacy - emails stay on your computer
- ✅ Unlimited usage

## 🔧 Troubleshooting

### "Ollama not running"
- **Windows**: Ollama should auto-start. Check system tray
- **Mac/Linux**: Run `ollama serve` in a terminal
- Check: Open http://localhost:11434 in browser - should say "Ollama is running"

### "Model not found"
```cmd
ollama pull llama3.2
```

### "Connection refused"
Make sure Ollama is running:
```cmd
ollama serve
```

### Want to switch models?
Edit `.env`:
```env
OLLAMA_MODEL=mistral    # or llama2, phi, etc.
```

Then pull the new model:
```cmd
ollama pull mistral
```

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama3.2 | 2GB | Medium | Great | Recommended |
| mistral | 4GB | Slower | Excellent | Best quality |
| llama2 | 3.8GB | Slow | Good | Balanced |
| phi | 1.6GB | Fast | Decent | Speed |

## 💡 Tips

1. **First run is slow** - Model loads into memory (30 seconds)
2. **Subsequent runs are fast** - Model stays in memory
3. **Restart Ollama** if it's slow: 
   ```cmd
   taskkill /f /im ollama.exe
   ollama serve
   ```

## 🔄 Switch Back to OpenAI

Edit `.env`:
```env
LLM_PROVIDER=openai
```

## ❓ Need Help?

Run the diagnostic:
```cmd
cd "d:\Projects\Email Productivity Agent"
py test_api.py
```

Check Ollama status:
```cmd
ollama list        # Show installed models
ollama ps          # Show running models
```

---

**Enjoy FREE unlimited AI! 🎉**
