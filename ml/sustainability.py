def calculate_sustainability(soil_score,erosion_score,irrigation,moisture,nitrogen,phosphorus,potassium):
    soil=round(max(0,min(100,soil_score))*.4,1)
    erosion=round(max(0,min(100,erosion_score))*.25,1)
    irrig=round({'Drip Irrigation':20,'Sprinkler Irrigation':16,'Flood Irrigation':9,'Rainfed':12,'None':5}.get(irrigation,10),1)
    moist=10 if 30<=moisture<=75 else 4
    nutrients=round(5*sum(v=='Medium' for v in (nitrogen,phosphorus,potassium))/3,1)
    total=round(soil+erosion+irrig+moist+nutrients,1)
    return {'score':total,'level':'Excellent' if total>=85 else 'Good' if total>=70 else 'Moderate' if total>=50 else 'Needs Improvement','soil_component':soil,'erosion_component':erosion,'irrigation_component':irrig,'moisture_component':moist,'nutrient_component':nutrients}
