from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'irrigation_model_candidate.joblib'

def predict_irrigation(measurements):
    """Experimental only. Soil moisture must match the training sensor's unknown scale."""
    bundle = joblib.load(MODEL_PATH)
    features = bundle['features']
    missing = [key for key in features if key not in measurements]
    if missing:
        raise ValueError(f'Missing measurements: {missing}')
    row = pd.DataFrame([{key: float(measurements[key]) for key in features}])
    model = bundle['model']
    predicted = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    return {
        'irrigation_required': bool(predicted),
        'predicted_label': predicted,
        'probability': {str(cls): float(p) for cls, p in zip(model.classes_, probabilities)},
        'warning': 'Experimental prediction; soil moisture units not verified.'
    }
