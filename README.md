# Face Recognition Platform with Real-Time AI Q&A using RAG
# FaceIQ - Automatic Face Recognition Web App

## 🚀 Overview

**FaceIQ** is an advanced face recognition web application that utilizes a live webcam feed to detect and identify faces in real-time. It draws bounding boxes and displays names on recognized faces as they appear in the frame. While the system processes video continuously, it requires initial user configuration or interaction to enable detection, making it semi-automated rather than fully automatic. The platform also features integration with a real-time AI Q&A system powered by Retrieval-Augmented Generation (RAG), allowing users to interact with the system for intelligent responses based on retrieved data.
---

## 🧠 Architecture Diagram

![Architecture Diagram](./Architecture_Design.png)

> **Note:** The above diagram illustrates the overall architecture of FaceIQ, showcasing interactions between the React frontend (camera UI), Node.js backend (API/WebSocket server), and Python-based face recognition engine (FastAPI). The face data is stored locally using formats like Pickle or JSON.

---

## 📹 Demo Video

🎥 **Watch the live demo:**  
[![FaceIQ Demo]([https://kumaragurudtsteam-my.sharepoint.com/:v:/g/personal/eraianbu_22ad_kct_ac_in/EREczrtOpEtJt89w53IznCoBV29cTzJhAH3HAmtrI6TUng?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DtA4kn)](https://kumaragurudtsteam-my.sharepoint.com/:v:/g/personal/eraianbu_22ad_kct_ac_in/EREczrtOpEtJt89w53IznCoBV29cTzJhAH3HAmtrI6TUng?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DtA4kn)


---

## 🛠️ How to Run Locally

Follow these steps to set up the project on your machine:

### 🔁 Clone the Repository
```bash
git clone https://github.com/your-username/Face-Recognition-Platform-with-RealTime-AI-Q-A-using-RAG.git
cd Face-Recognition-Platform-with-RealTime-AI-Q-A-using-RAG
```

### 📦 Install Frontend & Backend Dependencies
```bash
# Frontend (React)
cd client
npm install

# Backend (Node.js)
cd ../server
npm install
```

### 🧪 Set Up Python Environment for Face Recognition

1. Create a virtual environment (Python 3.10.13 recommended):
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows CMD**: `venv\Scripts\activate`
   - **PowerShell**: `.env\Scripts\Activate.ps1`
   - **Git Bash/Linux/Mac**: `source venv/Scripts/activate`
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

> ⚠️ **Note**: `dlib` may require Python 3.10.13 or older for compatibility.

---

### ▶️ Start the App

1. Start the backend server:
   ```bash
   node index.js
   ```

2. Start the frontend server:
   ```bash
   cd client
   $env:NODE_OPTIONS="--openssl-legacy-provider"
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`
4. Allow webcam access when prompted.

---

## 📬 Contact

Have questions or need support?  
📧 [eraianbu873@gmail.com](mailto:eraianbu873@gmail.com)  
🌐 [https://eraianbu.pages.dev](https://eraianbu.pages.dev)

This project is a part of a hackathon run by https://katomaran.com 
