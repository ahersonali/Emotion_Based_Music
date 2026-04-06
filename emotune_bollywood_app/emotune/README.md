# 🎵 EmoTune – Bollywood Emotion Music App

> Camera se emotion detect karo → Perfect Bollywood song suno!

---

## 🚀 FEATURES

- 📝 **Registration / Login** – Free account, secure password hashing
- 📷 **Live Camera** – Browser camera via JavaScript (no install needed)
- 🎭 **Emotion Detection** – face-api.js se 7 emotions: Happy, Sad, Angry, Surprised, Fearful, Disgusted, Neutral
- 👥 **Group Detection** – 2+ log camera mein → Group Anthem songs!
- 🎵 **Bollywood Songs Only** – Trending, 90s hits, 2000s classics
- 📱 **Mobile Friendly** – Responsive design, works on phone browser
- 🌐 **Free Hosting** – Render.com pe free deploy karo

---

## 📋 LOCAL SETUP (Apne Computer Pe)

### Step 1 – Python Check Karo
```bash
python --version
# Python 3.9+ chahiye
```

### Step 2 – Project Folder Mein Jao
```bash
cd emotune
```

### Step 3 – Virtual Environment Banao
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 – Dependencies Install Karo
```bash
pip install -r requirements.txt
```

### Step 5 – App Chalaao
```bash
python app.py
```

### Step 6 – Browser Mein Kholo
```
http://localhost:5000
```

---

## 📱 MOBILE PE KAISE DEKHO (Same WiFi Se)

1. `python app.py` chalaane ke baad terminal mein IP dikhega
2. Apne phone ke browser mein type karo:
   ```
   http://192.168.X.X:5000
   ```
   (X.X = aapka computer ka local IP)

### Apna IP kaise pata kare?
```bash
# Windows
ipconfig
# Mac/Linux  
ifconfig
```
`IPv4 Address` wala number use karo.

> ⚠️ Phone aur computer ek hi WiFi pe hone chahiye!

---

## 🌐 FREE HOSTING – RENDER.COM PE DEPLOY KARO

### Step 1 – GitHub Pe Upload Karo
1. GitHub.com pe account banao (free)
2. New repository banao → "emotune"
3. Yeh saare files upload karo

```bash
git init
git add .
git commit -m "EmoTune app"
git remote add origin https://github.com/AAPKA_USERNAME/emotune.git
git push -u origin main
```

### Step 2 – Render.com Account Banao
1. **render.com** pe jao
2. "Sign Up" → GitHub se login karo (free)

### Step 3 – Web Service Banao
1. Dashboard mein **"New +"** → **"Web Service"**
2. GitHub repo connect karo
3. Settings:
   - **Name:** emotune
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt && pip install gunicorn`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free ✅

### Step 4 – Deploy!
- "Create Web Service" click karo
- 2-3 minutes mein deploy hoga
- **Free URL milega:** `https://emotune.onrender.com`

> 📱 Yeh URL **kisi bhi phone** mein kaam karega – worldwide!

---

## 🔧 ALTERNATIVE FREE HOSTING OPTIONS

### Option A: Railway.app
1. railway.app → GitHub se login
2. "New Project" → "Deploy from GitHub repo"
3. Automatic deploy! Free tier available

### Option B: PythonAnywhere (Easiest)
1. pythonanywhere.com → Free account
2. Files upload karo
3. Web app banao → Flask → WSGI file configure karo

### Option C: Vercel (with some config)
- Not ideal for Flask, Render better hai

---

## 🎭 EMOTION → SONGS MAPPING

| Emotion | Hindi | Songs Type |
|---------|-------|-----------|
| 😄 Happy | Khushi | Badtameez Dil, London Thumakda |
| 😢 Sad | Udaas | Tum Hi Ho, Channa Mereya |
| 😠 Angry | Gussa | Zinda, Sultan, Dangal |
| 😲 Surprised | Hairaan | Chaiyya Chaiyya, Kajra Re |
| 😨 Fearful | Darr | Teri Meri Kahaani |
| 😒 Disgusted | Alag | Bekhayali, Tera Ban Jaunga |
| 😊 Neutral | Sukoon | Raataan Lambiyan, Kal Ho Naa Ho |

---

## 📁 PROJECT STRUCTURE

```
emotune/
├── app.py              # Main Flask app + Music Library
├── requirements.txt    # Python packages
├── Procfile           # For Render/Heroku deployment
├── render.yaml        # Render.com config
├── templates/
│   ├── auth.html      # Login + Registration page
│   ├── home.html      # Dashboard + song browser
│   └── detect.html    # Camera + emotion detection page
└── README.md          # Yeh file!
```

---

## 🎵 SONG CATEGORIES

### Trending (2013-2024)
Kesariya, Naatu Naatu, Tum Hi Ho, Badtameez Dil, Zinda, Bekhayali...

### 90s Hits  
Chaiyya Chaiyya, DDLJ, Pehla Nasha, Didi Tera Dewar, Darr...

### 2000s Classics
Kajra Re, Dhoom Machale, Rock On, Desi Girl, Rang De Basanti...

### Group Anthems (2+ Faces)
Jai Ho, Naatu Naatu, Gallan Goodiyaan, Balam Pichkari, Ghoomar...

---

## 🐛 TROUBLESHOOTING

**Camera kaam nahi kar raha?**
- Browser mein camera permission allow karo
- Chrome/Firefox use karo (Safari mein issue ho sakta hai)
- HTTPS pe host karo production mein (Render automatically karta hai)

**face-api.js load nahi ho raha?**
- Internet connection check karo (models CDN se aate hain)
- App automatically simulation mode mein chala jaata hai

**Mobile pe camera nahi khul raha?**
- Phone browser mein camera permission allow karo
- Settings → Site Settings → Camera → Allow

---

## 📞 HELP

Koi problem aaye toh:
1. Terminal mein error message copy karo
2. Stack Overflow pe search karo
3. Python Flask documentation: flask.palletsprojects.com

---

**Made with ❤️ for Bollywood lovers!** 🎵🇮🇳
