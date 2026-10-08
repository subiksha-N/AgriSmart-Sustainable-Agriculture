from pathlib import Path
import joblib
import pandas as pd
MODEL_PATH = Path(__file__).resolve().parents[1] / 'models' / 'fertilizer_model_candidate.joblib'
def load_fertilizer_model():
    if not MODEL_PATH.exists(): raise FileNotFoundError(f'Fertilizer model not found: {MODEL_PATH}')
    bundle = joblib.load(MODEL_PATH)
    missing = {'model','features','numeric','categorical','labels'} - set(bundle)
    if missing: raise ValueError(f'Missing model bundle keys: {missing}')
    return bundle
def predict_fertilizer(temperature,humidity,moisture,soil_type,crop_type,nitrogen,phosphorus,potassium):
    bundle=load_fertilizer_model(); features=list(bundle['features'])
    inputs={'Temperature':temperature,'Humidity':humidity,'Moisture':moisture,'Soil Type':soil_type,'Crop Type':crop_type,'Nitrogen':nitrogen,'Phosphorous':phosphorus,'Potassium':potassium}
    norm={k.strip().lower():v for k,v in inputs.items()}
    row={f:norm[str(f).strip().lower()] for f in features}
    df=pd.DataFrame([row],columns=features); model=bundle['model']; pred=model.predict(df)[0]
    conf=round(float(max(model.predict_proba(df)[0]))*100,2) if hasattr(model,'predict_proba') else None
    return {'fertilizer':str(pred),'confidence':conf,'note':bundle.get('note','Experimental only; input units and field validity unverified.')}
