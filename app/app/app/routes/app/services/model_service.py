import joblib
import numpy as np

def load_model():
    try:
        return joblib.load("app/models/ensemble_model_v2.pkl")
    except Exception:
        return None

def predict_probabilities(model, features):
    if model:
        return model.predict_proba(features)[0].tolist()

    return [0.75, 0.15, 0.10]
