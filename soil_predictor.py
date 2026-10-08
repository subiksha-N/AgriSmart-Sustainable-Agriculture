from pathlib import Path
import joblib
import pandas as pd
MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'soil_model.joblib'
def predict_soil_fertility(measurements):
    bundle = joblib.load(MODEL_PATH)
    features = bundle['features']
    missing = [f for f in features if f not in measurements]
    if missing: raise ValueError(f'Missing soil measurements: {missing}')
    frame = pd.DataFrame([{f:float(measurements[f]) for f in features}], columns=features)
    model = bundle['model']; predicted = int(model.predict(frame)[0]); probs = model.predict_proba(frame)[0]
    return {'class_id':predicted, 'label':f'Class {predicted}', 'confidence':round(float(max(probs)),4), 'probabilities':{str(cls):round(float(p),4) for cls,p in zip(model.classes_,probs)}}
