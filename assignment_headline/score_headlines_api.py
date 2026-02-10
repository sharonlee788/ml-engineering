from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get('/status')
def status():
    d = {'status': 'OK'}
    return d

class HeadlinesRequest(BaseModel):
    headlines: List[str]

# load model once
try:
    encoder = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
except Exception:
    encoder = SentenceTransformer("all-MiniLM-L6-v2")

svm_model = joblib.load("model/svm.joblib")

@app.post("/score_headlines")
def score_headlines(req: HeadlinesRequest):
    headlines = req.headlines

    # if empty list -> empty result
    if not headlines:
        logging.warning("score_headlines called with empty headlines list")
        return {"labels": []}
    
    try:
        vectors = encoder.encode(headlines)
        labels = svm_model.predict(vectors)
        return {"labels": list(labels)}
    except Exception:
        logging.error("Error occurred during headline scoring")
        return {"error": "Internal error"}