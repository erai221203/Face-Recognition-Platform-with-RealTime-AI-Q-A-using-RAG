const express = require('express');
const fs = require('fs');
const cors = require('cors');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const WebSocket = require('ws');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(bodyParser.json({ limit: '10mb' }));

const IMAGE_PATH = './temp.jpg';
const PY_ENV = {
  ...process.env,
  GROQ_API_KEY: process.env.GROQ_API_KEY,
};

// === Register Face API ===
app.post('/api/register', (req, res) => {
  const { image, name } = req.body;
  const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');
  fs.writeFileSync(IMAGE_PATH, base64Data, 'base64');

  const py = spawn('python', ['../backend/face_handler.py', 'register', name], { env: PY_ENV });

  py.stdout.on('data', (data) => {
    res.json({ message: data.toString().trim() });
  });

  py.stderr.on('data', (err) => {
    console.error("Python error:", err.toString());
    res.status(500).json({ error: "Python error", detail: err.toString() });
  });
});

// === Recognize Face API ===
app.post('/api/recognize', (req, res) => {
  const { image } = req.body;
  const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');
  fs.writeFileSync(IMAGE_PATH, base64Data, 'base64');

  const py = spawn('python', ['../backend/face_handler.py', 'recognize'], { env: PY_ENV });

  py.stdout.on('data', (data) => {
    try {
      const parsed = JSON.parse(data.toString());
      res.json(parsed);
    } catch (err) {
      console.error("JSON parse error:", err);
      res.status(500).json({ error: "Invalid response from Python" });
    }
  });

  py.stderr.on('data', (err) => {
    console.error("Python error:", err.toString());
    res.status(500).json({ error: "Python error", detail: err.toString() });
  });
});

// === Start HTTP Server ===
const server = app.listen(5000, () => {
  console.log('✅ Express server running on http://localhost:5000');
});

// === WebSocket Server ===
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  console.log("🔌 WebSocket connected");

  ws.on('message', (msg) => {
    console.log("📨 Received query:", msg.toString());
    const data = JSON.parse(msg.toString());

    const py = spawn('python', ['../backend/chat_handler.py', data.query], { env: PY_ENV });

    let output = '';
    py.stdout.on('data', (out) => {
      output += out.toString();
    });

    py.stdout.on('end', () => {
      console.log("🤖 Python reply:", output.trim());
      ws.send(JSON.stringify({ reply: output.trim() }));
    });

    py.stderr.on('data', (err) => {
      console.error("💥 Python error:", err.toString());
      ws.send(JSON.stringify({ error: err.toString() }));
    });
  });
});
