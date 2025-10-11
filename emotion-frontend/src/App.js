import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [emotion, setEmotion] = useState("");
  const [emoji, setEmoji] = useState("");

  const emojiMap = {
    joy: "😄",
    sadness: "😢",
    anger: "😠",
    fear: "😨",
    love: "❤️",
    surprise: "😲",
  };

  const handlePredict = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", { text });
      const emotionLabel = res.data.emotion;
      setEmotion(emotionLabel);
      setEmoji(emojiMap[emotionLabel] || "");
    } catch (err) {
      console.error("Prediction error:", err);
      setEmotion("error");
      setEmoji("");
    }
  };

  return (
    <div className="app-root">
      <header className="topbar">
        <div className="brand">
          <img src="/logo192.png" alt="logo" />
          <div>
            <h1>AI Text Emotion Classifier</h1>
            <p className="tag">Understand feelings in text — fast & friendly</p>
          </div>
        </div>
      </header>

      <main className="container">
        <section className="card">
          <label className="label">Enter text</label>
          <textarea
            className="input"
            rows={6}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type something like: I had a great day at work!"
          />

          <div className="controls">
            <button
              className="btn primary"
              onClick={handlePredict}
              disabled={!text.trim()}
            >
              Predict Emotion
            </button>
            <button
              className="btn secondary"
              onClick={() => { setText(""); setEmotion(""); setEmoji(""); }}
            >
              Clear
            </button>
          </div>

          {emotion && (
            <div className="result">
              <div className="result-badge">{emoji}</div>
              <div className="result-text">
                <div className="result-label">Predicted</div>
                <div className="result-value">{emotion}</div>
              </div>
            </div>
          )}
        </section>

        <aside className="info">
          <div className="info-card">
            <h3>Tips</h3>
            <ul>
              <li>Paste short sentences or social posts for best results.</li>
              <li>Try different phrasings to see how predictions change.</li>
              <li>The model runs on a local backend at <code>localhost:8000</code>.</li>
            </ul>
          </div>
        </aside>
      </main>

      <footer className="footer">Built with ❤️ — small demo app</footer>
    </div>
  );
}

export default App;
