def analyze_soil(ph,moisture,nitrogen,phosphorus,potassium):
    score=100; problems=[]; recommendations=[]
    if ph<5.5: score-=22; problems.append('Acidic soil'); recommendations.append('Confirm acidity with laboratory testing before applying amendments.')
    elif ph>7.5: score-=18; problems.append('Alkaline soil'); recommendations.append('Investigate alkalinity with local soil testing.')
    if moisture<30: score-=18; problems.append('Low moisture'); recommendations.append('Consider mulching and irrigation planning.')
    elif moisture>75: score-=18; problems.append('High moisture'); recommendations.append('Review drainage and avoid overwatering.')
    for label,value in [('Nitrogen',nitrogen),('Phosphorus',phosphorus),('Potassium',potassium)]:
        if value=='Low': score-=10; problems.append(f'Low {label}'); recommendations.append(f'Use soil-test-based {label.lower()} management.')
        elif value=='High': score-=5; problems.append(f'High {label}'); recommendations.append(f'Avoid unnecessary {label.lower()} inputs.')
    score=max(0,score)
    return {'score':score,'health':'Good' if score>=80 else 'Moderate' if score>=55 else 'Needs Attention','ph_status':'Acidic' if ph<5.5 else 'Alkaline' if ph>7.5 else 'Suitable range','moisture_status':'Low' if moisture<30 else 'High' if moisture>75 else 'Balanced','problems':problems,'recommendations':recommendations}
