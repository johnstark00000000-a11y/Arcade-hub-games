# ArcadeCraft Universal Game Engine 🚀

Production-ready Game Portal supporting Web Assembly, Pygbag (Python Pygame in Web), Java Applets/CheerpJ, HTML5, JavaScript, and CSS games.

## Quick Setup & Deployment to Render

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Universal Game Portal"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. Deploy on Render.com
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub Repository.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn server:app`
6. Under **Environment Variables**, add:
   - Key: `ADMIN_PIN`
   - Value: `YourSecretPinHere` (e.g. `9999`)
7. Click **Deploy Web Service**!

## Supporting Game Engines & Languages
- **Python (Pygame / Arcade):** Convert to Web assembly using `pygbag` (`pygbag main.py`) and upload the build zip file containing `index.html`.
- **Java / WebAssembly:** Upload bundled `.html` with `.js`/`.wasm` runners.
- **HTML5 / JS / CSS:** Direct zip/HTML paste.
