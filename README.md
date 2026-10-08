# AgriSmart — Smart Sustainable Agriculture Advisor

Run with Python 3.11–3.13:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The package includes the crop, soil fertility, fertilizer and irrigation model artifacts, along with compatible predictors. Original user files are not modified. Crop and soil laboratory units, fertilizer input units, soil class definitions and irrigation sensor calibration have not been independently verified. This is an educational prototype, not a field decision system. RUSLE uses user-entered site-specific factors.

For Streamlit Cloud, push this entire folder to a GitHub repository, set the main file to `app.py`, and keep `models/` tracked. Review scikit-learn model serialization compatibility if running a different version than used for training.
