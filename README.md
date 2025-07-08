# CPA Tracker

## 🚀 Run Locally
- `pip install -r requirements.txt`
- `python run.py`
- Visit http://localhost:5000
- Login with `admin` / `admin123`

## 💡 Postback Testing with ngrok
1. Install ngrok
2. Run: `ngrok http 5000`
3. Get public URL, e.g. `https://a1b2c3d4.ngrok.io`
4. In affiliate dashboard set:
`https://a1b2c3d4.ngrok.io/postback?click_id={click_id}&revenue={revenue}&country={country}`

## ☁️ Deploy on Render
1. Push to GitHub repo
2. On Render:
   - Click "New Web Service"
   - Connect repo
   - Env: Python
   - Build: `pip install -r requirements.txt`
   - Start: `python run.py`
3. Use new URL for your affiliate postback.

## 📊 Features
- Real-time dashboard (Chart.js)
- Admin offer add/delete
- Auto tracking links
- Global S2S GET postback
- Country + revenue + timestamp tracking
