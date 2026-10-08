def recommend_crops(soil_type, ph, moisture, temperature, rainfall):
    catalog=[('Rice',{'Clay','Loamy','Silty'},(5.5,7.5),(55,100),(20,38),(900,5000)),('Millets',{'Sandy','Red Soil','Loamy'},(5.0,8.5),(10,65),(20,42),(200,1200)),('Groundnut',{'Sandy','Red Soil','Loamy'},(5.5,7.5),(20,70),(20,38),(350,1100)),('Maize',{'Loamy','Black Soil','Silty'},(5.5,7.8),(30,80),(18,36),(450,1500)),('Cotton',{'Black Soil','Loamy','Red Soil'},(5.8,8.2),(20,75),(21,40),(400,1400)),('Wheat',{'Loamy','Clay','Silty'},(6,8),(25,75),(10,30),(250,1200)),('Sugarcane',{'Loamy','Clay','Black Soil'},(6,8),(45,90),(20,40),(900,2500))]
    output=[]
    for name,soils,p,m,t,r in catalog:
        score=20 if soil_type in soils else 5
        for value, bounds,weight in [(ph,p,20),(moisture,m,20),(temperature,t,20),(rainfall,r,20)]:
            score+=weight if bounds[0]<=value<=bounds[1] else max(0,weight-10)
        output.append({'crop':name,'score':min(100,round(score))})
    return sorted(output,key=lambda x:x['score'],reverse=True)[:5]
