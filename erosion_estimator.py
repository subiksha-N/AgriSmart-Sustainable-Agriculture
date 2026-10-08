def estimate_soil_erosion(r,k,ls,c,p):
    for key,value in {'R':r,'K':k,'LS':ls,'C':c,'P':p}.items():
        if float(value)<0: raise ValueError(f'{key} cannot be negative')
    loss=round(float(r)*float(k)*float(ls)*float(c)*float(p),3)
    risk='Low' if loss<5 else 'Moderate' if loss<10 else 'High' if loss<20 else 'Very High'
    tips=['Maintain ground cover and minimize bare soil','Use contour planting or appropriate erosion barriers']
    if loss>=10: tips+=['Consult a local soil conservation specialist for a site-specific plan']
    return {'soil_loss':loss,'unit':'tonnes/hectare/year','erosion_risk':risk,'recommendations':tips,'factors':{'R':r,'K':k,'LS':ls,'C':c,'P':p},'method':'RUSLE'}
