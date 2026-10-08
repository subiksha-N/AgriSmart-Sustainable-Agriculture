def analyze_conservation(soil_type,moisture,rainfall,land_slope,erosion,irrigation):
    risk_points={'Low':0,'Medium':20,'High':40}[erosion]+{'Flat':0,'Moderate':20,'Steep':40}[land_slope]+(15 if rainfall>1400 else 0)+(10 if soil_type=='Sandy' else 0)
    risk='High' if risk_points>=55 else 'Medium' if risk_points>=25 else 'Low'
    erosion_score=max(0,100-risk_points)
    need='High' if moisture<30 else 'Low' if moisture>75 else 'Moderate'
    water_status='Dry' if moisture<30 else 'Waterlogged risk' if moisture>75 else 'Adequate'
    efficiency={'Drip Irrigation':'High','Sprinkler Irrigation':'Moderate','Flood Irrigation':'Low','Rainfed':'Rain-dependent','None':'Not assessed'}.get(irrigation,'Not assessed')
    ir=['Check soil moisture and local crop requirements before irrigating','Use mulching to reduce evaporation']
    co=['Maintain vegetation or cover crops','Avoid leaving soil exposed after harvesting']
    if land_slope!='Flat': co+=['Consider contour farming or terracing where suitable']
    if risk=='High': co+=['Seek site-specific erosion control advice']
    return {'water_need':need,'water_status':water_status,'irrigation_efficiency':efficiency,'irrigation_recommendations':ir,'erosion_risk':risk,'erosion_score':erosion_score,'conservation_recommendations':co}
