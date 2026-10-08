import streamlit as st
import pandas as pd
from datetime import datetime
from recommendation import recommend_crops
from soil_analysis import analyze_soil
from conservation import analyze_conservation
from sustainability import calculate_sustainability
from report_generator import generate_pdf_report
from ml.predictor import predict_crop
from ml.soil_predictor import predict_soil_fertility
from ml.fertilizer_predictor import predict_fertilizer
from ml.irrigation_predictor import predict_irrigation
from erosion_estimator import estimate_soil_erosion
# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Smart Sustainable Agriculture Advisor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }
    h1 {
        color: #2E7D32;
    }
    h2, h3 {
        color: #388E3C;
    }
    [data-testid="stMetric"] {
        background-color: rgba(46, 125, 50, 0.08);
        border: 1px solid rgba(46, 125, 50, 0.25);
        padding: 15px;
        border-radius: 12px;
        min-height: 125px;
    }
    /* Show long metric values fully instead of truncating them */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    [data-testid="stMetricValue"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.15 !important;
        word-break: normal !important;
    }
    [data-testid="stMetricLabel"] {
        white-space: normal !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        line-height: 1.2 !important;
        font-size: clamp(1.05rem, 1.6vw, 1.65rem) !important;
    }
    [data-testid="stForm"] {
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(46, 125, 50, 0.20);
    }
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
    }
    .hero-card {
        padding: 25px;
        border-radius: 16px;
        background-color: rgba(46, 125, 50, 0.07);
        border: 1px solid rgba(46, 125, 50, 0.25);
        margin-bottom: 20px;
    }
    .best-crop-card {
        text-align: center;
        padding: 28px;
        border-radius: 16px;
        background-color: rgba(76, 175, 80, 0.10);
        border: 2px solid rgba(76, 175, 80, 0.30);
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .score-card {
        text-align: center;
        padding: 25px;
        border-radius: 16px;
        background-color: rgba(46, 125, 50, 0.08);
        border: 2px solid rgba(46, 125, 50, 0.25);
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --forest:#173f30; --sage:#e8f0e7; --gold:#c6a76b; }
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif; }
.stApp { background: linear-gradient(180deg,#f5f6ef 0%,#f8faf6 45%,#f4f6f1 100%); color:#20392d; }
.block-container { max-width:1370px; padding-top:1.6rem; padding-bottom:4rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:#173f30 !important; }
h1 { font-weight:800 !important; font-size:clamp(2rem,4vw,3.1rem) !important; margin-bottom:1.2rem !important; }
h2 { margin-top:1.5rem !important; }
[data-testid="stSidebar"] { background:#183e2f; }
[data-testid="stSidebar"] * { color:#e9f3e9 !important; }
[data-testid="stSidebar"] hr { border-color:#50725b; }
[data-testid="stForm"] { border:1px solid #dce7da; border-radius:20px; background:rgba(255,255,255,.94); padding:1.4rem 1.6rem; box-shadow:0 12px 42px rgba(25,66,47,.055); }
[data-testid="stMetric"] { background:white !important; border:1px solid #dce8dc !important; border-radius:16px !important; box-shadow:0 5px 22px rgba(28,64,41,.045); padding:18px !important; }
[data-testid="stMetricLabel"] { color:#617466 !important; }
[data-testid="stMetricValue"] { color:#184834 !important; font-weight:800 !important; }
.stButton button[kind="primary"],.stFormSubmitButton button { background:#205840 !important; color:#fff !important; border:0 !important; border-radius:11px !important; min-height:3.1rem; font-weight:700; }
.stDownloadButton button { background:#205840 !important; color:white !important; border-radius:11px !important; }
[data-testid="stTabs"] button { font-weight:650; }
[data-testid="stAlert"] { border-radius:12px; }
.agri-banner {position:relative; overflow:hidden; border-radius:22px; min-height:185px; padding:28px 36px; margin:0 0 24px; background:linear-gradient(105deg,rgba(17,51,35,.96),rgba(28,85,55,.83)),url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1600&q=85') center 55%/cover; box-shadow:0 12px 30px rgba(14,52,30,.15); color:white; }
.agri-banner .eyebrow {letter-spacing:.22em; font-size:.68rem; font-weight:800; color:#d6c58d; margin-bottom:12px; }
.agri-banner .headline {font:800 clamp(1.55rem,3vw,2.3rem)/1.2 'Manrope',sans-serif; max-width:650px; color:white; letter-spacing:-.04em; }
.agri-banner .fine {color:#e4f1e6; margin-top:12px; font-size:.9rem; }
@media(max-width:750px){.agri-banner{padding:22px;min-height:160px;} [data-testid="stForm"]{padding:.7rem;} }
</style>
""",unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.title("🌱 AgriSmart")
    st.write(
        "**Smart Sustainable Agriculture Advisor**"
    )
    st.caption(
        "Crop Recommendation & Soil Conservation System"
    )
    st.divider()
    st.subheader("📌 System Modules")
    st.write("🌾 Crop Recommendation")
    st.write("🧪 Soil Health Analysis")
    st.write("🌿 Nutrient Management")
    st.write("🤖 ML Soil Fertility Prediction")
    st.write("💧 Irrigation Advisor")
    st.write("🏞️ Erosion Risk Assessment")
    st.write("🌱 Soil Conservation")
    st.write("♻️ Sustainability Analysis")
    st.write("🎯 Priority Action Plan")
    st.write("📄 Farm Report")
    st.divider()
    st.info(
        "This application provides educational decision support "
        "for sustainable farm and soil management."
    )
# ============================================================
# HEADER
# ============================================================
st.title("Smart Sustainable Agriculture Advisor")
st.markdown("""<div class="agri-banner"><div class="eyebrow">AGRISMART  /  FARM INTELLIGENCE</div><div class="headline">Better decisions start with healthier soil.</div><div class="fine">Crop insights &nbsp;•&nbsp; Soil diagnostics &nbsp;•&nbsp; Water & conservation</div></div>""", unsafe_allow_html=True)

# ============================================================
# INPUT FORM
# ============================================================
st.header("📋 Farm & Soil Information")
with st.form("farm_analysis_form"):
    # ========================================================
    # SOIL INFORMATION
    # ========================================================
    st.subheader("🌍 Soil Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        soil_type = st.selectbox(
            "Soil Type",
            [
                "Loamy",
                "Clay",
                "Sandy",
                "Silty",
                "Red Soil",
                "Black Soil"
            ]
        )
    with col2:
        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )
    with col3:
        moisture = st.slider(
            "Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=50
        )
    # ========================================================
    # NUTRIENT INFORMATION
    # ========================================================
    st.subheader("🌿 Soil Nutrient Status")
    st.caption(
        "Select nutrient status according to the available soil-test report."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        nitrogen = st.selectbox(
            "Nitrogen (N)",
            [
                "Low",
                "Medium",
                "High"
            ]
        )
    with col2:
        phosphorus = st.selectbox(
            "Phosphorus (P)",
            [
                "Low",
                "Medium",
                "High"
            ]
        )
    with col3:
        potassium = st.selectbox(
            "Potassium (K)",
            [
                "Low",
                "Medium",
                "High"
            ]
        )
    # ========================================================
    # ENVIRONMENT
    # ========================================================
    st.subheader("🌦️ Environmental Conditions")
    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=60.0,
            value=27.0,
            step=0.5
        )
    with col2:
        rainfall = st.number_input(
            "Annual / Seasonal Rainfall (mm)",
            min_value=0.0,
            max_value=5000.0,
            value=800.0,
            step=10.0
        )
    with col3:
        land_slope = st.selectbox(
            "Land Slope",
            [
                "Flat",
                "Moderate",
                "Steep"
            ]
        )
    # ========================================================
    # FARMING CONDITIONS
    # ========================================================
    st.subheader("🚜 Current Farming Conditions")
    col1, col2 = st.columns(2)
    with col1:
        erosion = st.selectbox(
            "Observed Soil Erosion",
            [
                "Low",
                "Medium",
                "High"
            ]
        )
    with col2:
        irrigation = st.selectbox(
            "Current Irrigation Method",
            [
                "Drip Irrigation",
                "Sprinkler Irrigation",
                "Flood Irrigation",
                "Rainfed",
                "None"
            ]
        )
    st.write("")
    st.divider()
    st.subheader("🤖 Machine Learning Crop Prediction Inputs")
    st.caption(
        "Enter measured N, P and K values in the same units as the training dataset, "
        "along with relative humidity. Do not convert Low/Medium/High categories into "
        "numbers without a validated soil-test conversion."
    )
    ml_col1, ml_col2, ml_col3, ml_col4 = st.columns(4)
    with ml_col1:
        ml_n = st.number_input("ML Nitrogen (N)", min_value=0, max_value=200, value=90)
    with ml_col2:
        ml_p = st.number_input("ML Phosphorus (P)", min_value=0, max_value=200, value=42)
    with ml_col3:
        ml_k = st.number_input("ML Potassium (K)", min_value=0, max_value=250, value=43)
    with ml_col4:
        ml_humidity = st.number_input(
            "Relative Humidity (%)", min_value=0.0, max_value=100.0, value=80.0
        )
    st.caption(
        "The crop dataset's N/P/K measurement units and rainfall period must match "
        "your actual inputs. The original dataset does not document all field conditions."
    )
    # Independent laboratory measurements for experimental soil ML.
    st.divider()
    st.subheader("🤖 ML Soil Fertility Prediction Inputs")
    st.caption(
        "Enter all 12 laboratory measurements before clicking Analyze Farm, using the exact units "
        "and methods of the training dataset. These fields are separate from "
        "the Low/Medium/High nutrient status above."
    )
    soil_ml_features = ["N", "P", "K", "ph", "ec", "oc", "S", "zn", "fe", "cu", "Mn", "B"]
    soil_ml_measurements = {}
    st.warning(
        "Dataset feature units and fertility-class definitions have not been "
        "verified. Use this only with compatible laboratory data for demonstration."
    )
    soil_input_columns = st.columns(4)
    for index, feature in enumerate(soil_ml_features):
        with soil_input_columns[index % 4]:
            soil_ml_measurements[feature] = st.number_input(
                f"Soil ML: {feature}",
                min_value=0.0,
                max_value=1000000.0,
                value=6.5 if feature == "ph" else 0.0,
                step=0.1,
                format="%.2f",
                key=f"soil_ml_{feature}",
            )
    st.caption("Enter actual measured values; the initial defaults are placeholders, not sample results.")

    st.divider()
    st.subheader("Fertilizer model inputs")
    st.caption("Experimental dataset-specific inputs. Numeric values must match the training data measurement scale; no fertilizer dose is calculated.")
    fert_cols = st.columns(4)
    with fert_cols[0]:
        fert_soil = st.selectbox("Fertilizer soil category", ["Loamy", "Black", "Clayey", "Red", "Sandy"])
    with fert_cols[1]:
        fert_crop = st.selectbox("Fertilizer crop category", ["Paddy", "Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds", "Pulses", "Sugarcane", "Tobacco", "Wheat"])
    with fert_cols[2]:
        fert_moisture = st.number_input("Fertilizer dataset moisture", min_value=0.0, max_value=1000.0, value=38.0)
    with fert_cols[3]:
        fert_humidity = st.number_input("Fertilizer dataset humidity (%)", min_value=0.0, max_value=100.0, value=52.0)
    st.caption("For fertilizer ML, the numeric N/P/K inputs from Crop ML above are reused. Check their units against the fertilizer dataset before interpreting results.")
    st.divider()
    st.subheader("Irrigation sensor model inputs")
    st.caption("Raw sensor readings are not moisture percentages. This experimental model was trained only for Paddy and Groundnut.")
    irr_cols = st.columns(4)
    with irr_cols[0]:
        irr_crop = st.selectbox("Sensor model crop", ["Paddy", "Groundnut"])
    with irr_cols[1]:
        irr_days = st.number_input("Crop age (days)", min_value=0, max_value=365, value=45)
    with irr_cols[2]:
        irr_sensor = st.number_input("Raw soil moisture sensor reading", min_value=0.0, max_value=10000.0, value=450.0)
    with irr_cols[3]:
        irr_soil_temp = st.number_input("Soil temperature (°C)", min_value=-10.0, max_value=70.0, value=26.0)
    st.divider()
    st.subheader("RUSLE erosion factors")
    st.caption("Enter locally determined R, K, LS, C and P factors. These illustrative defaults are not calibrated to your farm.")
    rusle_cols = st.columns(5)
    with rusle_cols[0]: r_factor = st.number_input("R — rainfall erosivity", min_value=0.0, value=300.0)
    with rusle_cols[1]: k_factor = st.number_input("K — soil erodibility", min_value=0.0, value=0.03, format="%.3f")
    with rusle_cols[2]: ls_factor = st.number_input("LS — slope factor", min_value=0.0, value=2.0)
    with rusle_cols[3]: c_factor = st.number_input("C — cover factor", min_value=0.0, max_value=1.0, value=0.3)
    with rusle_cols[4]: p_factor = st.number_input("P — practice factor", min_value=0.0, max_value=1.0, value=0.5)

    analyze = st.form_submit_button(
        "🔍 Analyze Farm",
        use_container_width=True
    )
# ============================================================
# ANALYSIS
# ============================================================
if analyze:
    # ========================================================
    # RUN ANALYSIS ENGINES
    # ========================================================
    soil_ml_result = None
    soil_ml_error = None
    if any(soil_ml_measurements[feature] == 0.0 for feature in soil_ml_features if feature != "ph"):
        soil_ml_error = (
            "Enter actual laboratory measurements for all 12 soil fields before "
            "using the experimental fertility model. Zero placeholders are not valid measurements."
        )
    else:
        try:
            soil_ml_result = predict_soil_fertility(soil_ml_measurements)
        except (FileNotFoundError, KeyError, ValueError, OSError, TypeError) as exc:
            soil_ml_error = str(exc)

    ml_predictions = None
    ml_error = None
    try:
        ml_predictions = predict_crop(
            n=ml_n, p=ml_p, k=ml_k, temperature=temperature,
            humidity=ml_humidity, ph=ph, rainfall=rainfall, top_k=3
        )
    except (FileNotFoundError, KeyError, ValueError, OSError) as exc:
        ml_error = str(exc)
    fertilizer_result = None
    fertilizer_error = None
    try:
        fertilizer_result = predict_fertilizer(
            temperature=temperature, humidity=fert_humidity, moisture=fert_moisture,
            soil_type=fert_soil, crop_type=fert_crop,
            nitrogen=ml_n, phosphorus=ml_p, potassium=ml_k
        )
    except Exception as exc:
        fertilizer_error = str(exc)

    irrigation_ml_result = None
    irrigation_ml_error = None
    try:
        irrigation_ml_result = predict_irrigation({
            "CropType": 1 if irr_crop == "Paddy" else 2,
            "CropDays": irr_days, "Soil Moisture": irr_sensor,
            "Soil Temperature": irr_soil_temp,
            "Temperature": temperature, "Humidity": ml_humidity
        })
    except Exception as exc:
        irrigation_ml_error = str(exc)

    rusle_result = None
    rusle_error = None
    try:
        rusle_result = estimate_soil_erosion(r_factor, k_factor, ls_factor, c_factor, p_factor)
    except Exception as exc:
        rusle_error = str(exc)

    crop_results = recommend_crops(
        soil_type,
        ph,
        moisture,
        temperature,
        rainfall
    )
    soil_result = analyze_soil(
        ph,
        moisture,
        nitrogen,
        phosphorus,
        potassium
    )
    conservation_result = analyze_conservation(
        soil_type,
        moisture,
        rainfall,
        land_slope,
        erosion,
        irrigation
    )
    sustainability_result = calculate_sustainability(
        soil_result["score"],
        conservation_result["erosion_score"],
        irrigation,
        moisture,
        nitrogen,
        phosphorus,
        potassium
    )
    # ========================================================
    # IMPORTANT VALUES
    # ========================================================
    sustainability_score = sustainability_result["score"]
    sustainability_level = sustainability_result["level"]
    best_crop = crop_results[0]["crop"]
    best_crop_score = crop_results[0]["score"]
    # ========================================================
    # BUILD PRIORITY ACTION PLAN
    # ========================================================
    priority_actions = []
    # pH
    if ph < 5.5:
        priority_actions.append(
            "HIGH PRIORITY: Address acidic soil based on a proper "
            "soil test and local agricultural guidance."
        )
    elif ph > 7.5:
        priority_actions.append(
            "HIGH PRIORITY: Manage alkaline soil using appropriate "
            "soil-test-based practices."
        )
    # Moisture
    if moisture < 30:
        priority_actions.append(
            "HIGH PRIORITY: Improve soil moisture using appropriate "
            "irrigation and mulching."
        )
    elif moisture > 75:
        priority_actions.append(
            "HIGH PRIORITY: Reduce unnecessary irrigation and "
            "improve soil drainage."
        )
    # Nitrogen
    if nitrogen == "Low":
        priority_actions.append(
            "Improve nitrogen management using compost, green manure "
            "or legume-based crop rotation."
        )
    elif nitrogen == "High":
        priority_actions.append(
            "Avoid unnecessary nitrogen application and continue "
            "monitoring nutrient levels."
        )
    # Phosphorus
    if phosphorus == "Low":
        priority_actions.append(
            "Improve phosphorus management according to "
            "soil-test guidance."
        )
    elif phosphorus == "High":
        priority_actions.append(
            "Avoid unnecessary phosphorus application."
        )
    # Potassium
    if potassium == "Low":
        priority_actions.append(
            "Improve potassium management according to "
            "soil-test guidance."
        )
    elif potassium == "High":
        priority_actions.append(
            "Avoid unnecessary potassium application."
        )
    # Erosion
    if conservation_result["erosion_risk"] == "High":
        priority_actions.append(
            "HIGH PRIORITY: Implement erosion-control measures such "
            "as cover crops, mulching, vegetative barriers and "
            "appropriate slope management."
        )
    elif conservation_result["erosion_risk"] == "Medium":
        priority_actions.append(
            "Use preventive erosion-control practices such as "
            "cover crops and mulching."
        )
    # Irrigation
    if irrigation == "Flood Irrigation":
        priority_actions.append(
            "Consider switching from flood irrigation to a more "
            "water-efficient irrigation method where practical."
        )
    # No major problem
    if not priority_actions:
        priority_actions.append(
            "Current farm conditions are generally favorable. "
            "Continue monitoring soil health, moisture and nutrients."
        )
    # ========================================================
    # DASHBOARD HEADER
    # ========================================================
    st.divider()
    st.title("📊 Smart Farm Analysis Dashboard")
    st.success(
        "✅ Farm analysis completed successfully."
    )
    # ========================================================
    # TABS
    # ========================================================
    (
        overview_tab,
        crop_tab,
        soil_tab,
        water_tab,
        conservation_tab,
        sustainability_tab
    ) = st.tabs(
        [
            "📊 Overview",
            "🌾 Crops",
            "🧪 Soil",
            "💧 Water",
            "🏞️ Conservation",
            "♻️ Sustainability"
        ]
    )
    # ========================================================
    # TAB 1 - OVERVIEW
    # ========================================================
    with overview_tab:
        st.header("📌 Farm Health Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Soil Health",
                f"{soil_result['score']}/100"
            )
        with col2:
            st.metric(
                "Sustainability",
                f"{sustainability_score}/100"
            )
        with col3:
            st.metric(
                "Erosion Risk",
                conservation_result["erosion_risk"]
            )
        with col4:
            st.metric(
                "Water Requirement",
                conservation_result["water_need"]
            )
        # ----------------------------------------------------
        # BEST CROP
        # ----------------------------------------------------
        st.divider()
        st.subheader("🌾 Best Recommended Crop")
        st.html(f"""<div class="best-crop-card"><h2>🌾 {best_crop}</h2><h1>{best_crop_score}%</h1><p>Estimated Crop Suitability</p></div>""")
        if best_crop_score >= 80:
            st.success(
                "✅ Highly Suitable"
            )
        elif best_crop_score >= 60:
            st.warning(
                "⚠️ Moderately Suitable"
            )
        else:
            st.error(
                "⚠️ Low suitability under the entered conditions."
            )
        # ----------------------------------------------------
        # ACTION PLAN
        # ----------------------------------------------------
        st.divider()
        st.subheader("🎯 Priority Action Plan")
        for number, action in enumerate(
            priority_actions,
            start=1
        ):
            st.write(
                f"**{number}.** {action}"
            )
        # ----------------------------------------------------
        # FARM SUMMARY
        # ----------------------------------------------------
        st.divider()
        st.subheader("📋 Farm Condition Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Soil Type",
                soil_type
            )
        with col2:
            st.metric(
                "Soil pH",
                ph
            )
        with col3:
            st.metric(
                "Moisture",
                f"{moisture}%"
            )
        with col4:
            st.metric(
                "Temperature",
                f"{temperature} °C"
            )
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Rainfall",
                f"{rainfall:.0f} mm"
            )
        with col2:
            st.metric(
                "Slope",
                land_slope
            )
        with col3:
            st.metric(
                "Observed Erosion",
                erosion
            )
        with col4:
            st.metric(
                "Irrigation",
                irrigation
            )
    # ========================================================
    # TAB 2 - CROP RECOMMENDATION
    # ========================================================
    with crop_tab:
        st.subheader("🤖 Machine Learning Crop Recommendations")
        if ml_error:
            st.error(f"ML model unavailable: {ml_error}")
        elif ml_predictions:
            st.success(f"Predicted crop: {ml_predictions[0]['crop'].title()}")
            ml_table = pd.DataFrame([
                {
                    "Crop": result["crop"].title(),
                    "Model probability (%)": round(result["model_probability"] * 100, 2)
                }
                for result in ml_predictions
            ])
            st.dataframe(ml_table, use_container_width=True, hide_index=True)
            st.bar_chart(ml_table, x="Crop", y="Model probability (%)")
            st.caption(
                "These are Random Forest class probabilities, not validated field "
                "suitability percentages. The model does not use soil type, moisture "
                "or land slope, and may not generalize to local farms."
            )
        else:
            st.info("Enter crop measurements and click Analyze Farm to view ML results.")
        st.divider()
        st.subheader("🌾 Existing Rule-Based Crop Recommendations")
        st.header("🌾 Crop Recommendation")
        st.write(
            """
            Crops are ranked using a weighted rule-based suitability
            score based on soil type, pH, moisture, temperature
            and rainfall.
            """
        )
        # ----------------------------------------------------
        # CROP CARDS
        # ----------------------------------------------------
        crop_col1, crop_col2, crop_col3 = st.columns(3)
        crop_columns = [
            crop_col1,
            crop_col2,
            crop_col3
        ]
        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]
        for i, recommendation in enumerate(crop_results):
            crop = recommendation["crop"]
            score = recommendation["score"]
            with crop_columns[i % len(crop_columns)]:
                st.subheader(
                    f"{medals[i] if i < len(medals) else '🌿'} {crop}"
                )
                st.metric(
                    "Suitability",
                    f"{score}%"
                )
                st.progress(
                    min(
                        max(
                            float(score) / 100,
                            0.0
                        ),
                        1.0
                    )
                )
                if score >= 80:
                    st.success(
                        "Highly Suitable"
                    )
                elif score >= 60:
                    st.warning(
                        "Moderately Suitable"
                    )
                else:
                    st.error(
                        "Low Suitability"
                    )
        # ----------------------------------------------------
        # CROP CHART
        # ----------------------------------------------------
        st.divider()
        st.subheader("📊 Crop Suitability Comparison")
        crop_chart_data = pd.DataFrame(
            {
                "Crop": [
                    item["crop"]
                    for item in crop_results
                ],
                "Suitability (%)": [
                    item["score"]
                    for item in crop_results
                ]
            }
        )
        st.bar_chart(
            crop_chart_data,
            x="Crop",
            y="Suitability (%)"
        )
        st.info(
            "💡 The suitability percentage is a weighted "
            "rule-based score, not an ML prediction probability."
        )
        st.caption(
            "Actual crop selection should also consider season, "
            "crop variety, local climate, water availability, "
            "soil-test results and agricultural guidance."
        )
    # ========================================================
    # TAB 3 - SOIL HEALTH
    # ========================================================
    with soil_tab:
        st.header("🧪 Soil Health Analysis")
        st.divider()
        st.subheader("🤖 Experimental ML Soil Fertility Prediction")
        if soil_ml_error:
            st.error(f"Soil fertility model unavailable: {soil_ml_error}")
        elif soil_ml_result is not None:
            st.metric("Predicted fertility category", soil_ml_result["label"])
            st.metric("Estimated model probability", f"{soil_ml_result['confidence'] * 100:.1f}%")
            soil_probability_table = pd.DataFrame([
                {"Fertility class": f"Class {class_id}", "Model probability (%)": round(prob * 100, 2)}
                for class_id, prob in soil_ml_result["probabilities"].items()
            ])
            st.dataframe(soil_probability_table, use_container_width=True, hide_index=True)
            st.bar_chart(soil_probability_table, x="Fertility class", y="Model probability (%)")
            st.warning(
                "Experimental model only. Class 0/1/2 meanings and laboratory units "
                "must be confirmed from the dataset documentation. Probabilities are "
                "not calibrated confidence guarantees. Class 2 has only 39 unique "
                "profiles in the training dataset. Do not use this output to select fertilizers."
            )
        else:
            st.info("Enter the 12 soil measurements and click Analyze Farm to view the result.")
        st.caption("The rule-based soil health score above is separate from this ML classification.")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Health Score",
                f"{soil_result['score']}/100"
            )
        with col2:
            st.metric(
                "Overall Health",
                soil_result["health"]
            )
        with col3:
            st.metric(
                "pH Status",
                soil_result["ph_status"]
            )
        with col4:
            st.metric(
                "Moisture Status",
                soil_result["moisture_status"]
            )
        st.write("**Overall Soil Health**")
        st.progress(
            min(
                max(
                    soil_result["score"] / 100,
                    0.0
                ),
                1.0
            )
        )
        # ----------------------------------------------------
        # NUTRIENTS
        # ----------------------------------------------------
        st.divider()
        st.subheader("🌿 Nutrient Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Nitrogen (N)",
                nitrogen
            )
        with col2:
            st.metric(
                "Phosphorus (P)",
                phosphorus
            )
        with col3:
            st.metric(
                "Potassium (K)",
                potassium
            )
        # ----------------------------------------------------
        # SOIL PROBLEMS
        # ----------------------------------------------------
        st.divider()
        st.subheader("⚠️ Detected Soil Issues")
        if soil_result["problems"]:
            for problem in soil_result["problems"]:
                st.warning(
                    "⚠️ " + problem
                )
        else:
            st.success(
                "✅ No major soil issues were identified "
                "from the entered parameters."
            )
        # ----------------------------------------------------
        # SOIL RECOMMENDATIONS
        # ----------------------------------------------------
        st.subheader(
            "🌱 Soil & Nutrient Management Recommendations"
        )
        if soil_result["recommendations"]:
            for recommendation in soil_result[
                "recommendations"
            ]:
                st.info(
                    "✓ " + recommendation
                )
        else:
            st.success(
                "Maintain current soil-management practices "
                "and continue periodic soil testing."
            )
    # ========================================================
    # TAB 4 - WATER MANAGEMENT
    # ========================================================
    with water_tab:
        st.header("💧 Smart Irrigation Advisor")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Water Requirement",
                conservation_result["water_need"]
            )
        with col2:
            st.metric(
                "Water Status",
                conservation_result["water_status"]
            )
        with col3:
            st.metric(
                "Irrigation Efficiency",
                conservation_result[
                    "irrigation_efficiency"
                ]
            )
        # ----------------------------------------------------
        # CURRENT WATER CONDITIONS
        # ----------------------------------------------------
        st.divider()
        st.subheader("🌧️ Current Water Conditions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Soil Moisture",
                f"{moisture}%"
            )
        with col2:
            st.metric(
                "Rainfall",
                f"{rainfall:.0f} mm"
            )
        with col3:
            st.metric(
                "Irrigation Method",
                irrigation
            )
        # ----------------------------------------------------
        # IRRIGATION RECOMMENDATIONS
        # ----------------------------------------------------
        st.divider()
        st.subheader("💡 Irrigation Recommendations")
        for recommendation in conservation_result[
            "irrigation_recommendations"
        ]:
            st.info(
                "💧 " + recommendation
            )
        if moisture < 30:
            st.warning(
                "Low soil moisture detected. Water-management "
                "measures should be prioritized."
            )
        elif moisture > 75:
            st.warning(
                "High soil moisture detected. Reduce unnecessary "
                "irrigation and check drainage."
            )
        else:
            st.success(
                "Soil moisture is currently within a moderate range."
            )
    # ========================================================
    # TAB 5 - CONSERVATION
    # ========================================================
    with conservation_tab:
        st.header("🏞️ Soil Conservation & Erosion")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Erosion Risk",
                conservation_result[
                    "erosion_risk"
                ]
            )
        with col2:
            st.metric(
                "Erosion Risk Score",
                f"{conservation_result['erosion_score']}/100"
            )
        st.write("**Erosion Risk Level**")
        st.progress(
            min(
                max(
                    conservation_result[
                        "erosion_score"
                    ] / 100,
                    0.0
                ),
                1.0
            )
        )
        # ----------------------------------------------------
        # EROSION MESSAGE
        # ----------------------------------------------------
        if conservation_result["erosion_risk"] == "High":
            st.error(
                "🚨 High erosion risk detected. "
                "Soil-conservation measures should be prioritized."
            )
        elif conservation_result["erosion_risk"] == "Medium":
            st.warning(
                "⚠️ Moderate erosion risk detected. "
                "Preventive conservation practices are recommended."
            )
        else:
            st.success(
                "✅ Current erosion risk is relatively low."
            )
        # ----------------------------------------------------
        # LAND CONDITIONS
        # ----------------------------------------------------
        st.divider()
        st.subheader("📍 Land Conditions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Land Slope",
                land_slope
            )
        with col2:
            st.metric(
                "Observed Erosion",
                erosion
            )
        with col3:
            st.metric(
                "Rainfall",
                f"{rainfall:.0f} mm"
            )
        # ----------------------------------------------------
        # CONSERVATION RECOMMENDATIONS
        # ----------------------------------------------------
        st.divider()
        st.subheader(
            "🌱 Recommended Soil Conservation Practices"
        )
        for recommendation in conservation_result[
            "conservation_recommendations"
        ]:
            st.success(
                "✓ " + recommendation
            )
    # ========================================================
    # TAB 6 - SUSTAINABILITY
    # ========================================================
    with sustainability_tab:
        st.header("♻️ Overall Sustainability Assessment")
        # ----------------------------------------------------
        # MAIN SCORE
        # ----------------------------------------------------
        st.html(f"""<div class="score-card"><h3>Sustainability Score</h3><h1>{sustainability_score}/100</h1><h3>{sustainability_level}</h3></div>""")
        st.progress(
            min(
                max(
                    sustainability_score / 100,
                    0.0
                ),
                1.0
            )
        )
        # ----------------------------------------------------
        # SCORE MESSAGE
        # ----------------------------------------------------
        if sustainability_score >= 85:
            st.success(
                "🌟 Excellent sustainability performance. "
                "Continue maintaining efficient soil, water "
                "and conservation practices."
            )
        elif sustainability_score >= 70:
            st.success(
                "✅ Good sustainability performance. "
                "A few improvements can further increase "
                "farm sustainability."
            )
        elif sustainability_score >= 50:
            st.warning(
                "⚠️ Moderate sustainability performance. "
                "Improvement is recommended in soil, irrigation "
                "or conservation practices."
            )
        else:
            st.error(
                "🚨 Sustainability needs improvement. "
                "Priority should be given to soil health, "
                "water management and erosion control."
            )
        # ----------------------------------------------------
        # COMPONENT METRICS
        # ----------------------------------------------------
        st.divider()
        st.subheader("📊 Sustainability Components")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Soil Health",
                f"{sustainability_result['soil_component']}/40"
            )
        with col2:
            st.metric(
                "Erosion Management",
                f"{sustainability_result['erosion_component']}/25"
            )
        with col3:
            st.metric(
                "Irrigation",
                f"{sustainability_result['irrigation_component']}/20"
            )
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Moisture Management",
                f"{sustainability_result['moisture_component']}/10"
            )
        with col2:
            st.metric(
                "Nutrient Balance",
                f"{sustainability_result['nutrient_component']}/5"
            )
        # ----------------------------------------------------
        # NORMALIZED SUSTAINABILITY CHART
        # ----------------------------------------------------
        st.divider()
        st.subheader("📈 Sustainability Performance Analysis")
        sustainability_chart = pd.DataFrame(
            {
                "Component": [
                    "Soil Health",
                    "Erosion Management",
                    "Irrigation",
                    "Moisture",
                    "Nutrient Balance"
                ],
                "Performance (%)": [
                    round(
                        (
                            sustainability_result[
                                "soil_component"
                            ] / 40
                        ) * 100,
                        1
                    ),
                    round(
                        (
                            sustainability_result[
                                "erosion_component"
                            ] / 25
                        ) * 100,
                        1
                    ),
                    round(
                        (
                            sustainability_result[
                                "irrigation_component"
                            ] / 20
                        ) * 100,
                        1
                    ),
                    round(
                        (
                            sustainability_result[
                                "moisture_component"
                            ] / 10
                        ) * 100,
                        1
                    ),
                    round(
                        (
                            sustainability_result[
                                "nutrient_component"
                            ] / 5
                        ) * 100,
                        1
                    )
                ]
            }
        )
        st.bar_chart(
            sustainability_chart,
            x="Component",
            y="Performance (%)"
        )
        # ----------------------------------------------------
        # SCORE EXPLANATION
        # ----------------------------------------------------
        st.divider()
        st.subheader("🧮 How the Score is Calculated")
        st.write(
            """
            The educational sustainability index uses the
            following weighted components:
            - **40% — Soil Health**
            - **25% — Erosion Management**
            - **20% — Irrigation Efficiency**
            - **10% — Moisture Management**
            - **5% — Nutrient Balance**
            """
        )
        st.caption(
            "The sustainability score is an educational index "
            "created for this decision-support application. "
            "It is not a scientifically validated farm certification score."
        )
    # ========================================================
    # FINAL ACTION PLAN
    # ========================================================
    st.divider()
    st.header("🎯 Final Recommended Action Plan")
    st.write(
        """
        The following actions are prioritized according to the
        problems detected from the entered farm conditions.
        """
    )
    for number, action in enumerate(
        priority_actions,
        start=1
    ):
        if "HIGH PRIORITY" in action:
            st.warning(
                f"{number}. {action}"
            )
        else:
            st.info(
                f"{number}. {action}"
            )
    st.divider()
    st.header("Advanced farm intelligence")
    advanced_tabs = st.tabs(["Fertilizer model", "Irrigation sensor model", "RUSLE soil loss"])
    with advanced_tabs[0]:
        if fertilizer_result:
            a, b = st.columns(2)
            a.metric("Experimental fertilizer class", fertilizer_result["fertilizer"])
            b.metric("Model probability", f'{fertilizer_result["confidence"]:.1f}%' if fertilizer_result["confidence"] is not None else "N/A")
            st.caption("This is a dataset classification, not a fertilizer application recommendation or dose. Model training data are limited.")
        else:
            st.warning(f"Fertilizer model unavailable: {fertilizer_error}")
    with advanced_tabs[1]:
        if irrigation_ml_result:
            st.metric("Sensor model prediction", "Irrigation required" if irrigation_ml_result["irrigation_required"] else "Irrigation not required")
            st.caption("Experimental model only. Raw sensor scale is uncalibrated and the prediction is not a real irrigation schedule.")
            st.write("Class probabilities:", irrigation_ml_result["probability"])
        else:
            st.warning(f"Irrigation model unavailable: {irrigation_ml_error}")
    with advanced_tabs[2]:
        if rusle_result:
            a, b = st.columns(2)
            a.metric("Estimated annual soil loss", f'{rusle_result["soil_loss"]:.2f} t/ha/year')
            b.metric("Illustrative risk category", rusle_result["erosion_risk"])
            st.caption("RUSLE = R × K × LS × C × P. Results are only as reliable as the site-specific factors entered.")
            for advice in rusle_result["recommendations"]: st.write("• " + advice)
        else:
            st.warning(f"RUSLE calculation unavailable: {rusle_error}")

    # ========================================================
    # PROFESSIONAL PDF REPORT
    # ========================================================
    st.divider()
    st.header("📄 Professional Farm Analysis Report")
    st.write(
        """
        Generate and download a structured PDF containing the
        complete farm assessment, crop recommendations, soil-health
        analysis, irrigation guidance, conservation measures,
        sustainability assessment and priority action plan.
        """
    )
    pdf_report = generate_pdf_report(
        soil_type=soil_type,
        ph=ph,
        moisture=moisture,
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        temperature=temperature,
        rainfall=rainfall,
        land_slope=land_slope,
        erosion=erosion,
        irrigation=irrigation,
        crop_results=crop_results,
        soil_result=soil_result,
        conservation_result=conservation_result,
        sustainability_result=sustainability_result,
        priority_actions=priority_actions,
        ml_predictions=ml_predictions,
        soil_ml_result=soil_ml_result,
        fertilizer_result=fertilizer_result,
        irrigation_ml_result=irrigation_ml_result,
        rusle_result=rusle_result
    )
    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )
    with col2:
        st.download_button(
            label="📥 Download Professional PDF Report",
            data=pdf_report,
            file_name="Smart_Agriculture_Farm_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    st.caption(
        "The PDF contains the complete results of the current "
        "farm analysis."
    )
    # ========================================================
    # FINAL DISCLAIMER
    # ========================================================
    st.divider()
    st.caption(
        "ℹ️ Educational decision-support application. Results are "
        "estimates derived from the entered parameters and should not "
        "replace laboratory soil testing, current local weather data "
        "or professional agricultural advice."
    )
# ============================================================
# BEFORE ANALYSIS MESSAGE
# ============================================================
else:
    st.info(
        "👆 Enter the farm conditions above and click "
        "**Analyze Farm** to generate the complete analysis."
    )
