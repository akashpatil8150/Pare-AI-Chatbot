# 🚀 Render Deployment Guide - Pare AI Chatbot

## ✅ Pre-Deployment Checklist

All files have been prepared and configured for Render deployment:

- ✅ **Procfile** - Tells Render how to start your app with gunicorn
- ✅ **runtime.txt** - Specifies Python 3.11.9
- ✅ **requirements.txt** - Updated with gunicorn and all dependencies
- ✅ **app.py** - Production-ready with:
  - Dynamic PORT handling
  - host="0.0.0.0" for external access
  - Production logging
  - Health check endpoint
  - Error handlers
  - No debug mode
- ✅ **.gitignore** - Prevents committing .env file with API key

## 📋 Step-by-Step Deployment Instructions

### Step 1: Push Changes to GitHub

First, commit and push all the new files to your GitHub repository:

```bash
# Check what files have changed
git status

# Add all the new deployment files
git add Procfile runtime.txt requirements.txt app.py DEPLOYMENT_GUIDE.md

# Commit the changes
git commit -m "Prepare for Render deployment - Add Procfile, runtime.txt, update app.py for production"

# Push to GitHub
git push origin main
```

**Note:** If your branch is named `master` instead of `main`, use:
```bash
git push origin master
```

### Step 2: Create Render Account & New Web Service

1. Go to [https://render.com](https://render.com)
2. Sign up or log in (you can use your GitHub account)
3. Click **"New +"** button in the top right
4. Select **"Web Service"**

### Step 3: Connect Your GitHub Repository

1. Click **"Connect a repository"**
2. If first time: Click **"Configure account"** to authorize Render to access your GitHub
3. Find and select your repository: **`akashpatil8150/Pare-AI-Chatbot`**
4. Click **"Connect"**

### Step 4: Configure Web Service Settings

Fill in the following settings:

#### Basic Settings:
- **Name:** `pare-ai-chatbot` (or any name you prefer)
  - This will be part of your URL: `pare-ai-chatbot.onrender.com`
- **Region:** Choose closest to your location (e.g., `Oregon (US West)` or `Frankfurt (EU)`)
- **Branch:** `main` (or `master` if that's your default branch)
- **Root Directory:** Leave blank (empty)
- **Runtime:** `Python 3`

#### Build & Deploy Settings:
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
  
- **Start Command:** 
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
  ```
  
  **Note:** This should auto-populate from your Procfile, but verify it matches!

#### Instance Type:
- **Free** (for testing) or **Starter** ($7/month for better performance)
  - Free tier: Spins down after 15 minutes of inactivity
  - Starter: Always on, faster, better for production

### Step 5: Add Environment Variables

**CRITICAL:** You must add your Gemini API key as an environment variable!

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add the following:

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | `AIzaSyAEz7hHGVPikDiDUZa9pBIlg8cg89Jug5s` |

**⚠️ SECURITY WARNING:** 
- Your API key is currently exposed in your `.env` file in this chat
- After deployment, consider regenerating your API key at: https://aistudio.google.com/app/apikey
- Never commit `.env` file to GitHub (it's already in .gitignore, good!)

### Step 6: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will now:
   - Clone your repository
   - Install Python 3.11.9
   - Install dependencies from requirements.txt
   - Start your app with gunicorn
   - Assign a public URL

### Step 7: Monitor Deployment

Watch the deployment logs in real-time:

- **Building...** - Installing dependencies (1-3 minutes)
- **Deploying...** - Starting your application
- **Live** - ✅ Deployment successful!

**Expected log output:**
```
==> Building...
Collecting flask==3.1.2
Collecting gunicorn==23.0.0
...
==> Deploying...
Starting gunicorn...
[INFO] Starting Pare AI Chatbot on port 10000
[INFO] API Key loaded successfully (length: 39 characters)
[INFO] Gemini API configured successfully
==> Your service is live 🎉
```

### Step 8: Test Your Deployment

Once deployment shows **"Live"**, test your application:

1. **Get your URL:** `https://pare-ai-chatbot.onrender.com` (or your chosen name)

2. **Test health check:**
   ```
   https://pare-ai-chatbot.onrender.com/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "service": "Pare AI Chatbot",
     "timestamp": "2026-05-16T..."
   }
   ```

3. **Test main page:**
   - Open `https://pare-ai-chatbot.onrender.com` in browser
   - You should see the Pare AI Chatbot interface
   - Try sending a message: "Tell me about INNOV+ series"
   - Try booking an appointment

## 🔧 Troubleshooting Common Issues

### Issue 1: Build Failed - "No module named 'X'"

**Cause:** Missing dependency in requirements.txt

**Solution:**
```bash
# Add the missing package to requirements.txt
echo "package-name==version" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push origin main
```

Render will auto-deploy on push.

### Issue 2: Application Error - "Application failed to respond"

**Cause:** App not binding to correct host/port

**Solution:** Already fixed! Your app.py now uses:
```python
host='0.0.0.0', port=int(os.getenv('PORT', 5000))
```

### Issue 3: "GEMINI_API_KEY not found"

**Cause:** Environment variable not set in Render

**Solution:**
1. Go to Render Dashboard → Your Service
2. Click **"Environment"** tab
3. Add `GEMINI_API_KEY` with your API key
4. Click **"Save Changes"**
5. Service will auto-redeploy

### Issue 4: "429 - Quota Exceeded"

**Cause:** Hit Gemini API free tier limit (60 requests/minute)

**Solution:**
- Wait 1 minute for quota reset
- Check usage: https://ai.google.dev/pricing
- Consider upgrading API plan if needed
- Monitor usage in your app (top-right corner)

### Issue 5: Slow First Response (Free Tier)

**Cause:** Free tier spins down after 15 minutes of inactivity

**Solution:**
- First request after inactivity takes 30-60 seconds (cold start)
- Subsequent requests are fast
- Upgrade to Starter plan ($7/month) for always-on service

### Issue 6: Static Files Not Loading (CSS/JS)

**Cause:** Incorrect static file paths

**Solution:** Already fixed! Your templates use:
```html
{{ url_for('static', filename='css/style.css') }}
{{ url_for('static', filename='js/script.js') }}
```

This works correctly on Render.

### Issue 7: CORS Errors

**Cause:** Cross-origin requests blocked

**Solution:** Already fixed! Your app.py has:
```python
from flask_cors import CORS
CORS(app)
```

## 📊 Monitoring Your Deployment

### View Logs:
1. Go to Render Dashboard → Your Service
2. Click **"Logs"** tab
3. See real-time application logs

**Useful log messages:**
- `[INFO] Starting Pare AI Chatbot on port 10000` - App started
- `[INFO] API Key loaded successfully` - API key configured
- `[INFO] Processing chat request` - User sent message
- `[ERROR] Chat error: ...` - Something went wrong

### View Metrics:
1. Click **"Metrics"** tab
2. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Health Checks:
Render automatically pings `/health` endpoint every 30 seconds to verify your app is running.

## 🔄 Updating Your Deployment

Render auto-deploys on every push to your main branch:

```bash
# Make changes to your code
# ... edit files ...

# Commit and push
git add .
git commit -m "Update feature X"
git push origin main

# Render automatically detects the push and redeploys
```

**Manual Deploy:**
1. Go to Render Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## 🎯 Production Optimizations

### 1. Increase Workers (for higher traffic)

Edit `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --log-level info
```

**Workers formula:** `(2 × CPU cores) + 1`
- Free tier: 0.5 CPU → 2 workers (current)
- Starter: 1 CPU → 3 workers
- Standard: 2 CPU → 5 workers

### 2. Add Database (for persistent appointments)

Currently, appointments are stored in memory and lost on restart.

**To add PostgreSQL:**
1. Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Create database
3. Add `DATABASE_URL` environment variable to your web service
4. Update app.py to use database instead of `APPOINTMENTS` list

### 3. Add Redis (for caching)

Speed up responses by caching common queries.

### 4. Custom Domain

1. Render Dashboard → Your Service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Add your domain (e.g., `pareai.com`)
4. Update DNS records as instructed

### 5. Enable Auto-Deploy

Already enabled by default! Every push to main branch triggers deployment.

**To disable:**
1. Settings → **"Build & Deploy"**
2. Toggle **"Auto-Deploy"** off

## 📱 Testing Checklist

After deployment, test all features:

- [ ] Homepage loads correctly
- [ ] Chat interface appears
- [ ] Can send messages and get AI responses
- [ ] Product buttons work (INNOV+, DURA+, etc.)
- [ ] Can open "Book Appointment" modal
- [ ] Can select date and time
- [ ] Can submit appointment booking
- [ ] Appointment appears in chat
- [ ] Can view appointments list
- [ ] Can cancel appointments
- [ ] Time slots update correctly
- [ ] No console errors (F12 → Console)
- [ ] Works on mobile devices
- [ ] CSS and JavaScript load correctly

## 🔐 Security Best Practices

1. **Regenerate API Key** after deployment (since it was exposed in .env)
   - Go to: https://aistudio.google.com/app/apikey
   - Create new key
   - Update in Render environment variables

2. **Never commit .env file** (already in .gitignore ✅)

3. **Use environment variables** for all secrets (already implemented ✅)

4. **Enable HTTPS** (Render provides this automatically ✅)

5. **Monitor API usage** to prevent unexpected charges

## 📞 Support & Resources

- **Render Documentation:** https://render.com/docs
- **Render Status:** https://status.render.com
- **Gemini API Docs:** https://ai.google.dev/docs
- **Flask Documentation:** https://flask.palletsprojects.com
- **Your GitHub Repo:** https://github.com/akashpatil8150/Pare-AI-Chatbot

## 🎉 Success!

Once deployed, your Pare AI Chatbot will be live at:

**`https://pare-ai-chatbot.onrender.com`**

Share this URL with anyone - your chatbot is now publicly accessible!

---

**Need Help?** Check the troubleshooting section above or review Render logs for error messages.

**Made with ❤️ for Pare Interior & Exterior Solutions**
