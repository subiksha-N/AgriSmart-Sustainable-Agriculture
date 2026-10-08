from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'crop_model.joblib'


def predict_crop(n, p, k, temperature, humidity, ph, rainfall, top_k=3):
    """Return ranked crop predictions and model probabilities (not field guarantees)."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError('Train the model first: python -m ml.train_crop')
    artifact = joblib.load(MODEL_PATH)  # Only load model files you generated/trust.
    model, features = artifact['model'], artifact['features']
    row = pd.DataFrame([{
        'N': n, 'P': p, 'K': k, 'temperature': temperature,
        'humidity': humidity, 'ph': ph, 'rainfall': rainfall
    }], columns=features)
    probabilities = model.predict_proba(row)[0]
    ranked = sorted(zip(model.classes_, probabilities), key=lambda item: item[1], reverse=True)
    return [{'crop': crop, 'model_probability': round(float(prob), 4)}
            for crop, prob in ranked[:top_k]]
