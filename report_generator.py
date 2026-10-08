from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

def generate_pdf_report(soil_type,ph,moisture,nitrogen,phosphorus,potassium,temperature,rainfall,land_slope,erosion,irrigation,crop_results,soil_result,conservation_result,sustainability_result,priority_actions,ml_predictions=None,soil_ml_result=None,fertilizer_result=None,irrigation_ml_result=None,rusle_result=None):
    buffer=BytesIO(); doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title='AgriSmart Farm Assessment')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='AgTitle',parent=styles['Title'],fontSize=24,leading=29,textColor=colors.HexColor('#173F30'),spaceAfter=7))
    styles.add(ParagraphStyle(name='AgSection',parent=styles['Heading2'],fontSize=13,leading=17,textColor=colors.HexColor('#215C43'),spaceBefore=15,spaceAfter=8))
    styles.add(ParagraphStyle(name='AgBody',parent=styles['BodyText'],fontSize=9,leading=14,spaceAfter=6))
    styles.add(ParagraphStyle(name='AgNote',parent=styles['BodyText'],fontSize=8,leading=12,textColor=colors.HexColor('#586B60'),spaceAfter=7))
    story=[]
    def para(t,style='AgBody'): story.append(Paragraph(escape(str(t)),styles[style]))
    def section(t): para(t,'AgSection')
    def table(rows):
        cleaned=[[Paragraph(escape(str(cell)),styles['AgBody']) for cell in row] for row in rows]
        t=Table(cleaned,colWidths=[(174*mm)/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCEAE0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F9F6')]),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#215C43')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7)]))
        story.append(t);story.append(Spacer(1,8))
    para('AGRISMART | FARM INTELLIGENCE','AgTitle')
    para('Farm assessment • '+datetime.now().strftime('%d %B %Y'),'AgNote')
    para('Educational decision-support report. Predictions and scores are not substitutes for verified laboratory tests or local agronomic advice.','AgNote')
    section('01  Farm profile')
    table([['Field','Recorded value'],['Soil type',soil_type],['Soil pH',ph],['Soil moisture (%)',moisture],['N / P / K status',f'{nitrogen} / {phosphorus} / {potassium}'],['Air temperature',f'{temperature} °C'],['Rainfall',f'{rainfall} mm (user-specified period)'],['Land slope',land_slope],['Observed erosion',erosion],['Irrigation method',irrigation]])
    section('02  Crop suitability • rule-based')
    table([['Crop','Suitability index']]+[[r['crop'],f"{r['score']} / 100"] for r in crop_results[:5]])
    para('Suitability indices are heuristic scores, not model probabilities.','AgNote')
    section('03  Crop recommendation • machine learning')
    if ml_predictions: table([['Crop','Model probability']]+[[r['crop'],f"{r['model_probability']*100:.1f}%"] for r in ml_predictions])
    else: para('No ML crop result available.')
    section('04  Soil health and fertility')
    table([['Assessment','Value'],['Rule-based health score',f"{soil_result['score']}/100"],['Health level',soil_result['health']],['pH status',soil_result['ph_status']],['Moisture status',soil_result['moisture_status']]])
    if soil_ml_result:
        para(f"Experimental soil ML classification: {soil_ml_result['label']} (model probability {soil_ml_result['confidence']*100:.1f}%).")
    else: para('Experimental soil ML prediction unavailable (check laboratory measurements).')
    para('Soil ML class definitions and measurement units are not verified; classes are shown as numeric IDs.','AgNote')
    for x in soil_result['problems']: para('Issue: '+x)
    for x in soil_result['recommendations']: para('Guidance: '+x)
    section('05  Fertilizer • experimental ML')
    if fertilizer_result: para(f"Model selection: {fertilizer_result['fertilizer']} (model probability {fertilizer_result['confidence']}%).")
    else: para('No fertilizer ML prediction available.')
    para('Not a fertilizer dosage or application recommendation. Dataset is small and units are unverified.','AgNote')
    section('06  Water and irrigation')
    table([['Water requirement','Water status','Irrigation efficiency'],[conservation_result['water_need'],conservation_result['water_status'],conservation_result['irrigation_efficiency']]])
    if irrigation_ml_result: para('Experimental sensor-model classification: '+('Irrigation required' if irrigation_ml_result['irrigation_required'] else 'Not required')+'.')
    else: para('No sensor-based irrigation prediction available.')
    para('The irrigation ML input is an uncalibrated raw sensor reading, NOT soil moisture percentage.','AgNote')
    for x in conservation_result['irrigation_recommendations']: para('• '+x)
    section('07  Erosion and conservation')
    para(f"Rule-based erosion risk: {conservation_result['erosion_risk']}; erosion-management score: {conservation_result['erosion_score']}/100.")
    if rusle_result: para(f"RUSLE estimated annual soil loss: {rusle_result['soil_loss']:.3f} tonnes/hectare/year; educational risk category: {rusle_result['erosion_risk']}.")
    else: para('RUSLE result unavailable.')
    para('RUSLE estimates require site-calibrated R, K, LS, C and P factors. The provided inputs are not automatically derived from farm descriptors.','AgNote')
    for x in conservation_result['conservation_recommendations']: para('• '+x)
    section('08  Sustainability')
    para(f"Educational sustainability score: {sustainability_result['score']}/100 — {sustainability_result['level']}.")
    table([['Component','Weighted points'],['Soil health',f"{sustainability_result['soil_component']}/40"],['Erosion management',f"{sustainability_result['erosion_component']}/25"],['Irrigation efficiency',f"{sustainability_result['irrigation_component']}/20"],['Moisture management',f"{sustainability_result['moisture_component']}/10"],['Nutrient balance',f"{sustainability_result['nutrient_component']}/5"]])
    section('09  Priority action plan')
    for i,x in enumerate(priority_actions,1): para(f'{i}. {x}')
    section('10  Interpretation and limitations')
    para('The sustainability score is an educational weighted index and is not a certified environmental performance measure. Model probabilities are not validated field reliability scores. Consult agricultural experts and current local weather information before making crop, fertilizer or irrigation decisions.','AgNote')
    doc.build(story); out=buffer.getvalue();buffer.close();return out
