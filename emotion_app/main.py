from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import os

# ------------------------------
# Initialize FastAPI app
# ------------------------------
app = FastAPI(title="Emotion Classifier API - Ensemble")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Request schema
# ------------------------------
class TextInput(BaseModel):
    text: str

# ------------------------------
# Load Ensemble Components
# ------------------------------
_model_dir = "model"  # folder where all models are saved

try:
    # BiLSTM model
    bilstm_model = load_model(os.path.join(_model_dir, "bilstm_model.h5"))

    # Tokenizer and Label Encoder
    with open(os.path.join(_model_dir, "tokenizer.pkl"), "rb") as f:
        tokenizer = pickle.load(f)
    with open(os.path.join(_model_dir, "label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)

    # Naive Bayes and TF-IDF vectorizer
    with open(os.path.join(_model_dir, "naive_bayes_model.pkl"), "rb") as f:
        nb_model = pickle.load(f)
    with open(os.path.join(_model_dir, "tfidf_vectorizer.pkl"), "rb") as f:
        tfidf = pickle.load(f)

except Exception as e:
    raise RuntimeError(f"Failed to load ensemble components: {e}")

# ------------------------------
# Helper function - Ensemble Prediction
# ------------------------------
def predict_emotion_ensemble(texts, max_len=100):
    # BiLSTM predictions
    seq = tokenizer.texts_to_sequences(texts)
    seq_pad = pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')
    bilstm_pred = np.argmax(bilstm_model.predict(seq_pad), axis=1)
    bilstm_labels = label_encoder.inverse_transform(bilstm_pred)

    # Naive Bayes predictions
    X_tfidf = tfidf.transform(texts)
    nb_pred = nb_model.predict(X_tfidf)

    # Simple ensemble: pick BiLSTM if disagreement
    final_pred = [b if b == n else b for b, n in zip(bilstm_labels, nb_pred)]
    return final_pred

# ------------------------------
# API Endpoints
# ------------------------------
@app.get("/")
async def home():
    return {"message": "Welcome to Emotion Classifier API 🚀 (Ensemble)"}

@app.post("/predict")
async def predict_emotion(data: TextInput):
    pred = predict_emotion_ensemble([data.text])[0]
    return {"emotion": pred}

# ------------------------------
# Run Uvicorn
# ------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
