# 🌐 How to Share Your Medical Diagnosis Prototype as a Live Website Link

Your project now has a complete **Web Application** ([`index.html`](file:///c:/Users/patha/OneDrive/Desktop/medical%20diagnosis/index.html)) with the full Forward Chaining Inference Engine and all 10 diseases built in.

Here are **3 easy ways** to get a public link so anyone (friends, classmates, professors) can test it on their phone or laptop:

---

## ⚡ Method 1: Netlify Drop (Fastest — 30 Seconds, No Coding, 100% Free)

You can turn this folder into a live website link **without writing any commands**:

1. Open your web browser and go to:  
   👉 **[https://app.netlify.com/drop](https://app.netlify.com/drop)**
2. Open your File Explorer to:  
   `c:\Users\patha\OneDrive\Desktop\medical diagnosis`
3. **Drag and drop** this entire `medical diagnosis` folder directly onto the Netlify webpage.
4. Netlify will deploy it in **5 seconds** and give you an instant public link like:  
   `https://sanjeevani-diagnosis-2026.netlify.app`
5. Copy that link and share it on WhatsApp or during your presentation! Anyone who clicks it can test all 10 diseases and forward chaining on their mobile phone.

---

## 🐙 Method 2: GitHub Pages (Permanent Free Student Portfolio Link)

If you have a GitHub account:

1. Go to [https://github.com/new](https://github.com/new) and create a new repository called:  
   `medical-diagnosis` (make it **Public**).
2. Upload all the files from this folder into the repository (especially `index.html`).
3. Click on **Settings** (top tab of your repo) $\rightarrow$ **Pages** (on the left menu).
4. Under **Branch**, select `main` and click **Save**.
5. In 1 minute, GitHub will give you a permanent live URL:  
   `https://<your-username>.github.io/medical-diagnosis/`

---

## 📱 Method 3: Instant Wi-Fi / Hotspot Sharing (No Internet Needed!)

If you are demonstrating in a college lab or classroom:

1. Double click **`run_web.bat`** (or run `python web_server.py`).
2. The terminal will display two URLs:
   ```
   [+] Local Access URL     : http://localhost:8000
   [+] Mobile/LAN Access URL : http://192.168.1.15:8000
   ```
3. Tell your classmates or professor to connect to your phone's Wi-Fi hotspot or lab Wi-Fi.
4. Have them type that **Mobile URL** (`http://192.168.1.X:8000`) into their phone's browser (Chrome or Safari).
5. The system will load on their phone instantly!

---

## 💻 Method 4: Test Locally on Your Own Computer

You don't even need internet to test the web app:
* **Option A:** Double click [`index.html`](file:///c:/Users/patha/OneDrive/Desktop/medical%20diagnosis/index.html) in your folder — it will open directly in Chrome/Edge!
* **Option B:** Double click [`run_web.bat`](file:///c:/Users/patha/OneDrive/Desktop/medical%20diagnosis/run_web.bat) to run the Python web server.
* **Option C:** In the Desktop GUI, click the **`🌐 Open Web Version`** button in the top toolbar!
