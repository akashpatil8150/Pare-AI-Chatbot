# ⚙️ Render Configuration - Quick Reference

## Exact Settings for Render Dashboard

Copy these settings exactly when creating your web service on Render:

### 🔧 Basic Configuration

| Setting | Value |
|---------|-------|
| **Name** | `pare-ai-chatbot` |
| **Region** | `Oregon (US West)` or closest to you |
| **Branch** | `main` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | `Python 3` |

### 📦 Build & Deploy

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info` |

### 🔐 Environment Variables

Click "Add Environment Variable" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `GEMINI_API_KEY` | `AIzaSyAEz7hHGVPikDiDUZa9pBIlg8cg89Jug5s` | ⚠️ Regenerate after deployment! |

### 💰 Instance Type

- **Free** - For testing (spins down after 15 min inactivity)
- **Starter ($7/month)** - Recommended for production (always on)

### 🔄 Auto-Deploy

- ✅ **Enabled** (deploys automatically on git push)

---

## 🚀 One-Command Deploy

After pushing to GitHub, Render will automatically:

1. ✅ Detect Python 3.11.9 from `runtime.txt`
2. ✅ Install dependencies from `requirements.txt`
3. ✅ Start app using `Procfile` configuration
4. ✅ Assign public URL: `https://pare-ai-chatbot.onrender.com`

## 📋 Pre-Deploy Git Commands

```bash
# Add all deployment files
git add Procfile runtime.txt requirements.txt app.py DEPLOYMENT_GUIDE.md RENDER_SETTINGS.md

# Commit changes
git commit -m "Add Render deployment configuration"

# Push to GitHub
git push origin main
```

## ✅ Verification URLs

After deployment, test these endpoints:

| Endpoint | URL | Expected Response |
|----------|-----|-------------------|
| **Homepage** | `https://pare-ai-chatbot.onrender.com/` | Chatbot interface |
| **Health Check** | `https://pare-ai-chatbot.onrender.com/health` | `{"status": "healthy", ...}` |
| **API Chat** | `POST https://pare-ai-chatbot.onrender.com/api/chat` | JSON response |

## 🔍 Expected Build Log Output

```
==> Cloning from https://github.com/akashpatil8150/Pare-AI-Chatbot...
==> Checking out commit abc123...
==> Using Python version 3.11.9 (from runtime.txt)
==> Running build command: pip install -r requirements.txt
Collecting flask==3.1.2
Collecting flask-cors==6.0.2
Collecting google-generativeai==0.8.6
Collecting python-dotenv==1.2.1
Collecting gunicorn==23.0.0
Successfully installed flask-3.1.2 flask-cors-6.0.2 ...
==> Build successful!
==> Starting service with: gunicorn app:app --bind 0.0.0.0:$PORT ...
[INFO] Starting Pare AI Chatbot on port 10000
[INFO] API Key loaded successfully (length: 39 characters)
[INFO] Gemini API configured successfully
==> Your service is live 🎉
```

## ⚠️ Common Mistakes to Avoid

1. ❌ **Wrong branch name** - Use `main` not `master` (or vice versa)
2. ❌ **Forgot environment variable** - Must add `GEMINI_API_KEY`
3. ❌ **Wrong start command** - Must match Procfile exactly
4. ❌ **Root directory set** - Should be blank/empty
5. ❌ **Wrong runtime** - Must select `Python 3`

## 🎯 Success Indicators

✅ Build status shows **"Live"** with green dot  
✅ Logs show `[INFO] Starting Pare AI Chatbot on port 10000`  
✅ Logs show `[INFO] Gemini API configured successfully`  
✅ Health check returns `{"status": "healthy"}`  
✅ Homepage loads with chatbot interface  
✅ Can send messages and get AI responses  

## 📞 Quick Links

- **Render Dashboard:** https://dashboard.render.com
- **Your GitHub Repo:** https://github.com/akashpatil8150/Pare-AI-Chatbot
- **Gemini API Keys:** https://aistudio.google.com/app/apikey
- **Render Docs:** https://render.com/docs/deploy-flask

---

**Ready to deploy?** Follow the steps in `DEPLOYMENT_GUIDE.md`!
