# ⚡ Quick Start - Deploy in 5 Minutes

## 🚀 Fast Track to Deployment

### Step 1: Push to GitHub (2 minutes)

```bash
# Check status
git status

# Add all deployment files
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Push
git push origin main
```

### Step 2: Create Render Service (2 minutes)

1. Go to: https://render.com/dashboard
2. Click: **"New +"** → **"Web Service"**
3. Connect: **`akashpatil8150/Pare-AI-Chatbot`**
4. Configure:

```
Name: pare-ai-chatbot
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: (auto-filled from Procfile)
```

### Step 3: Add Environment Variable (1 minute)

Click **"Add Environment Variable"**:

```
Key: GEMINI_API_KEY
Value: AIzaSyAEz7hHGVPikDiDUZa9pBIlg8cg89Jug5s
```

### Step 4: Deploy! (< 1 minute)

Click **"Create Web Service"**

Wait for: **"Your service is live 🎉"**

### Step 5: Test (< 1 minute)

Open: `https://pare-ai-chatbot.onrender.com`

---

## ✅ Success Checklist

- [ ] Git push successful
- [ ] Render build shows "Live"
- [ ] Health check works: `/health`
- [ ] Homepage loads
- [ ] Chat responds to messages
- [ ] Can book appointments

---

## 🆘 Quick Troubleshooting

### Build Failed?
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `runtime.txt` has `python-3.11.9`

### App Not Starting?
- Verify `GEMINI_API_KEY` is set in environment variables
- Check logs for error messages
- Ensure `Procfile` exists and is correct

### 404 Error?
- Wait 30 seconds for deployment to complete
- Hard refresh: `Ctrl + Shift + R`
- Check URL is correct

### API Not Working?
- Verify API key is valid: https://aistudio.google.com/app/apikey
- Check Gemini API quota: https://ai.google.dev/pricing
- Review logs for error messages

---

## 📚 Full Documentation

- **Complete Guide:** `DEPLOYMENT_GUIDE.md`
- **Settings Reference:** `RENDER_SETTINGS.md`
- **Changes Explained:** `CHANGES_SUMMARY.md`

---

## 🎯 Your URLs

After deployment:

- **Live App:** `https://pare-ai-chatbot.onrender.com`
- **Health Check:** `https://pare-ai-chatbot.onrender.com/health`
- **Render Dashboard:** `https://dashboard.render.com`
- **GitHub Repo:** `https://github.com/akashpatil8150/Pare-AI-Chatbot`

---

## 🔄 Update Deployment

```bash
# Make changes
# ... edit files ...

# Push to GitHub (auto-deploys)
git add .
git commit -m "Update X"
git push origin main
```

Render automatically redeploys on every push!

---

**Ready? Start with Step 1! 🚀**
