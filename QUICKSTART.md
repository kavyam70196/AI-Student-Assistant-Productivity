# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**Get your API key**: https://platform.openai.com/api-keys

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Test Each Feature

### Test Chatbot
- Click "Study Chatbot"
- Ask: "Explain photosynthesis in simple terms"

### Test Resume Builder
- Click "Resume Builder"
- Fill in your details
- Click "Generate Resume"

### Test Code Explainer
- Click "Code Explainer"
- Paste this code:
  ```python
  def factorial(n):
      if n == 0:
          return 1
      return n * factorial(n-1)
  ```
- Click "Explain Code"

### Test Notes Generator
- Click "Notes Generator"
- Paste any study material
- Click "Generate Notes"

---

## 💡 Tips

1. **Dark Mode**: Click the moon icon in sidebar
2. **Copy Results**: Use copy buttons on output sections
3. **Clear Chat**: Use "Clear Chat" button to reset conversation
4. **Mobile**: Works on mobile devices too!

---

## ⚠️ Common Issues

**Error: "No module named 'flask'"**
- Solution: Run `pip install -r requirements.txt`

**Error: "OpenAI API key not found"**
- Solution: Create `.env` file with your API key

**Error: "Port 5000 in use"**
- Solution: Change port in app.py to 5001 or another port

---

## 📞 Need Help?

Check the full README.md for detailed documentation.

Happy Learning! 🎓
