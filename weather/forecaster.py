import requests
from universal import uniutils as uni
from commands import speechtranslate as unitconv
import datetime
from universal import vars as universal
import calendar

weeklyData = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/2205%20West%20Canton%20Pl?unitGroup=us&key=BHFCCKY362XGLDYMK3FRKYZHB&include=obs%2Cfcst%2Calerts%2Ccurrent"
weeklyDataJSON = None

highPressureThresh = 1018
lowPressureThresh = 1013



def currentForecast():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day = weeklyDataJSON['currentConditions']
    if "alerts" in weeklyDataJSON:
        alert = weeklyDataJSON['alerts']
    dayName = unitconv.getDate("name")
    trueDegree = unitconv.degreeTranslate(['windir'])
    day = {
        "notes":None,
        "important":None,
        'takeaway':None,
        "temp": day['temp'],
        'fl': day['feelslike'],
        'humidity': day['humidity'],
        'dew': day['dew'],
        'pressure': day['pressure'],
        'uv': day['uvindex'] or 0,
    }
    day['takeaway'] = uni.choose(["favorable", "decent", "good", "okay"])

    if day['pressure'] <= lowPressureThresh:
        day['notes'] = uni.choose([
            f"The barometric pressure seems low, reading at only {day['pressure']} hectopascals.",
            f"Barometric pressure is reading fairly low at {day['pressure']} hectopascals.",
            f"Additionally; I am reading a low barometric reading of {day['pressure']} hectopascals."
        ])
    elif day['pressure'] >= highPressureThresh:
        day['notes'] = uni.choose([
            f"Another note, I am reading a high barometric reading of {day['pressure']} hectopascals.",
            f"The barometric reading for the area is high, reading in at {day['pressure']} hectopascals.",
            f"I've also noticed a rather high barometric reading, reading in at {day['pressure']} hectopascals."
        ])
    if day['uv'] > 8:
        day['imporant'] = uni.choose([
            "The UV reading is fairly high for the area.",
            "UV is reading fairly high right now.",
            "Addtionally; I am noticing a high UV reading."
        ])
    if day['humidity'] > 80:
        day['notes'] += uni.choose([
            "Also, humidity for the area is reading rather high, at a {day['humidity']}%.",
            "I am seeing a humidity reading of {day['humidity']}%.",
            "I've also noticed a rather high humidity reading."
        ])
    difference = day['temp'] - day['fl']

    phrase = uni.choose([
        f"The current conditions for today are {day['takeaway']} with temperatures around {day['temp']}°**.",
        f"Today seems {day['takeaway']} with temperatures currently at {day['temp']}°**.",
        f"The current temperature for today is {day['temp']}°**."
    ])
    if difference > 2 or difference < -2:
        phrase = phrase.replace("**", uni.choose[
            f" with it feeling like {day['temps']['fl']}°",
            f". The average feels-like temperature is {day['temps']['fl']}°",
            f" and feels-like temperatures around {day['temps']['fl']}°",
            f" and it will feel around {day['temps']['fl']}° outside",
            f" with feels like averaging {day['temps']['fl']}°",
            f" with feels like following at {day['temps']['fl']}°.",
            f" with feels like doing the same at {day['temps']['fl']}°.",
        ])
    else:
        phrase = phrase.replace("**", "")
    
    phrase += " " + (day['important'] or "") + (day['notes'] or "") 
    vars.weather['current'] = day
    return phrase


def dataProcess():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day = weeklyDataJSON['days'][0]
    dayName = unitconv.getDate("name")
    trueDegree = unitconv.degreeTranslate(day['winddir'])
    returnDay = {
        "notes": {},
        "important":{},
        "day": dayName,
        "dt": datetime.datetime.now(),
        "daynum": 0,
        "temps": {
            "day": round(day['temp']),
            "fl": round(day['feelslike'])},
        "details": {
            "pressure": round(day['pressure']),
            'humidity': round(day['humidity']),
            'dp': round(day['dew']),
            'uvi': round(day['uvindex']),
            'clouds': day["cloudcover"],
            'pop': day['precipprob'],
            'snow': day['snow'],
            'sv': day['severerisk'],
            'poptype': day['preciptype'],
            'windspeed': day['windspeed'],
            'winddir': trueDegree},
        "forecast": {
            "basic": day['conditions'],
            "details": day["description"],
            "icon": day["icon"]}}
    if returnDay['details']['uvi'] >= 8:
        returnDay['important']['uv'] = "high"
    if returnDay['details']['sv'] <= 50 and returnDay['details']['sv'] > 30:
        returnDay['important']['severe'] = 'moderate'
    elif returnDay['details']['sv'] > 50:
        returnDay['important']['severe'] = 'high'
    if returnDay['details']['pressure'] >= highPressureThresh:
        returnDay['notes']['pressure'] = 'high'
    elif returnDay['details']['pressure'] <= lowPressureThresh:
        returnDay['notes']['pressure'] = 'low'

    return returnDay

def phraseBuild(day):

    context = uni.choose(["fair", "good", "moderate", "acceptable", "adequate", "favorable", "opportune"])

    important = ""
    if 'important' in day:
        if 'uv' in day['important']:
            if day['important']['uv'] == "high":
                context = uni.choose(["sunny", "bright", "summery", "clear", "cloudless", "clement"])
                important += uni.choose([
                    "Additionally, the UV is fairly high today. Wear sunscreen.",
                    "It also seems like UV readings are fairly high today.",
                    "You'll also want to make note that the UV readings are high today.",
                    "Another important note for today, the UV readings are fairly high today."
                ])
        if 'severe' in day['important']:
            if day['important']['severe'] == "moderate":
                context = uni.choose(["tempestuous", "turbulent", "boisterous", "foul"])
                important += uni.choose([
                    "There is also a moderate threat of severe weather.",
                    "The forecast is also showing a moderate threat of severe weather.",
                    "I am also noting a moderate weather threat today."
                ])
            elif day['important']['severe'] == "high":
                context = uni.choose(["melancholic", "distressing", "parlous"])
                important += uni.choose([
                    "It seems like there will be a fairly high threat of severe weather.",
                    "You may also want to note that there is a high chance of severe weather today.",
                    "There also seems to be a high chance of severe weather today."
                ])
    
    notes = ""
    if 'notes' in day:
        if 'pressure' in day['notes']:
            if day['notes']['pressure'] == "high":
                notes += uni.choose([
                    "I've also noted a pressure reading on the higher end today.",
                    "I also noticing a high pressure reading today.",
                    "Furthermore, I've notice a rise in atmospheric pressure."])

            if day['notes']['pressure'] == "low":
                notes += uni.choose([
                    "There also is a decrease in pressure in this area. It seems lower than typical averages.",
                    "I also noticing a lower barometric pressure reading in the area.",
                    "Additionally; I've notice a decrease in barometric pressure."])


    beginning = uni.choose([
        f"Today's weather seems {context} with an average temperature of {day['temps']['day']}°**.",
        f"I'm forecasting a {context} day with temperatures around {day['temps']['day']}°**.",
        f"Today seems fairly {context} with temperatures around {day['temps']['day']}°**.",
        f"I forecast today to be {context} with temperatures at {day['temps']['day']}°**."
    ])
    difference = day['temps']['day'] - day['temps']['fl']
    if difference > 2 or difference < -2:
        beginning = beginning.replace("**", uni.choose[
            f". Expect it to feel like {day['temps']['fl']}°",
            f". The average feels-like temperature is {day['temps']['fl']}°",
            f"  and feels-like temperatures around {day['temps']['fl']}°",
            f" and it will feel around {day['temps']['fl']}° outside"
        ])
    else:
        beginning = beginning.replace("**", "")
    weatherResult = uni.choose([
        f"You'll notice it will be {day['forecast']['details']}",
        f"You should expect {day['forecast']['details']}",
        f"I am forecasting today to be {day['forecast']['details']}",
        f"Anticipate today's weather being {day['forecast']['details']}"
    ])

    mainPhrase = beginning + " <break time='0.5s'/> " + weatherResult + " <break time='0.5s'/> " + important + " <break time='0.5s'/> " + notes

    return mainPhrase 

def forecastInit(forecastUpdate):
    mainDay = dataProcess()
    mainPhrase = phraseBuild(mainDay)
    mainDay['phrase'] = mainPhrase

    if forecastUpdate:                          ## Universal Variable Hour Weather Update
        if universal.weather['pastDay']:
            dayTime = universal.weather['pastDay']['dt']
            if (dayTime + 86400) <= mainDay['dt']:
                universal.weather['pastDay'] = mainDay
        else:
            universal.weather['pastDay'] = mainDay
        universal.weather['day'] = mainDay
    
    return mainPhrase


def dataTomProcess():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day = weeklyDataJSON['days'][1]
    dayName = unitconv.getDay(1)
    trueDegree = unitconv.degreeTranslate(day['winddir'])
    returnDay = {
        "notes": {},
        "important":{},
        "day": dayName,
        "dt": datetime.datetime.now(),
        "daynum": 0,
        "temps": {
            "day": round(day['temp']),
            "fl": round(day['feelslike'])},
        "details": {
            "pressure": round(day['pressure']),
            'humidity': round(day['humidity']),
            'dp': round(day['dew']),
            'uvi': round(day['uvindex']),
            'clouds': day["cloudcover"],
            'pop': day['precipprob'],
            'snow': day['snow'],
            'sv': day['severerisk'],
            'poptype': day['preciptype'],
            'windspeed': day['windspeed'],
            'winddir': trueDegree},
        "forecast": {
            "basic": day['conditions'],
            "details": day["description"],
            "icon": day["icon"]}}
    if returnDay['details']['uvi'] >= 8:
        returnDay['important']['uv'] = "high"
    if returnDay['details']['sv'] <= 50 and returnDay['details']['sv'] > 30:
        returnDay['important']['severe'] = 'moderate'
    elif returnDay['details']['sv'] > 50:
        returnDay['important']['severe'] = 'high'
    if returnDay['details']['pressure'] >= highPressureThresh:
        returnDay['notes']['pressure'] = 'high'
    elif returnDay['details']['pressure'] <= lowPressureThresh:
        returnDay['notes']['pressure'] = 'low'

    return returnDay

def phraseTomBuild(day):

    context = uni.choose(["fair", "good", "moderate", "acceptable", "adequate", "favorable", "opportune"])

    important = ""
    if 'important' in day:
        if 'uv' in day['important']:
            if day['important']['uv'] == "high":
                context = uni.choose(["sunny", "bright", "summery", "clear", "cloudless", "clement"])
                important += uni.choose([
                    "Additionally, the UV will be fairly high tomorrow. You'll want to consider wearing sunscreen.",
                    "It also seems like UV readings are going to be fairly high tomorrow.",
                    "You'll also want to make note that the UV readings are expected to be high.",
                    "Another important note for tomorrow, the UV readings are fairly high."
                ])
        if 'severe' in day['important']:
            if day['important']['severe'] == "moderate":
                context = uni.choose(["tempestuous", "turbulent", "boisterous", "foul"])
                important += uni.choose([
                    "There is also a moderate threat of severe weather.",
                    "The forecast is also showing a moderate threat of severe weather.",
                    "I am also noting a moderate weather threat."
                ])
            elif day['important']['severe'] == "high":
                context = uni.choose(["melancholic", "distressing", "parlous"])
                important += uni.choose([
                    "It seems like there will be a fairly high threat of severe weather.",
                    "You may also want to note that there is a high chance of severe weather.",
                    "There also seems to be a high chance of severe weather."
                ])
    
    notes = ""
    if 'notes' in day:
        if 'pressure' in day['notes']:
            if day['notes']['pressure'] == "high":
                notes += uni.choose([
                    "I've also noted a pressure reading on the higher end.",
                    "I also noticing a high pressure reading.",
                    "Furthermore, I've notice a rise in atmospheric pressure."])

            if day['notes']['pressure'] == "low":
                notes += uni.choose([
                    "There also is a decrease in pressure in this area. It seems lower than typical averages.",
                    "I also noticing a lower barometric pressure reading in the area.",
                    "Additionally; I've notice a decrease in barometric pressure."])


    beginning = uni.choose([
        f"Tomorrow's weather seems {context} with an average temperature of {day['temps']['day']}°**.",
        f"I'm forecasting a {context} day tomorrow, with temperatures around {day['temps']['day']}°**.",
        f"Tomorrow seems fairly {context} with temperatures around {day['temps']['day']}°**.",
        f"I forecast tomorrow to be {context} with temperatures at {day['temps']['day']}°**."
    ])
    difference = day['temps']['day'] - day['temps']['fl']
    if difference > 2 or difference < -2:
        beginning = beginning.replace("**", uni.choose[
            f". Expect it to feel like {day['temps']['fl']}°",
            f". The average feels-like temperature is {day['temps']['fl']}°",
            f" and feels-like temperatures around {day['temps']['fl']}°",
            f" and it will feel around {day['temps']['fl']}° outside"
        ])
    else:
        beginning = beginning.replace("**", "")
    weatherResult = uni.choose([
        f"You'll notice it will be {day['forecast']['details']}",
        f"You should expect tomorrow to be {day['forecast']['details']}",
        f"I am forecasting tomorrow to be {day['forecast']['details']}",
        f"Anticipate tomorrow's weather being {day['forecast']['details']}"
    ])

    mainPhrase = beginning + " <break time='0.5s'/> " + weatherResult + " <break time='0.5s'/> " + important + " <break time='0.5s'/> " + notes

    return mainPhrase 

def forecastTomInit(forecastUpdate):
    mainDay = dataTomProcess()
    mainPhrase = phraseTomBuild(mainDay)
    mainDay['phrase'] = mainPhrase
    
    return mainPhrase

    
def data7Process():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day1 = weeklyDataJSON['days'][1]
    day2 = weeklyDataJSON['days'][2]
    day3 = weeklyDataJSON['days'][3]
    day4 = weeklyDataJSON['days'][4]
    day5 = weeklyDataJSON['days'][5]
    day6 = weeklyDataJSON['days'][6]
    day7 = weeklyDataJSON['days'][7]
    week = [day1, day2, day3, day4, day5, day6, day7]
    returnWeek = []
    for day in week:
        if 'zizdent' not in day:
            dayName = unitconv.getDay(week.index(day))
            trueDegree = unitconv.degreeTranslate(day['winddir'])
            returnDay = {
                "zizdent":True,
                "day": dayName,
                "daynum": week.index(day),
                "temps": {
                    "day": round(day['temp']),
                    "fl": round(day['feelslike'])},
                "details": {
                    "pressure": round(day['pressure']),
                    'humidity': round(day['humidity']),
                    'dp': round(day['dew']),
                    'uvi': round(day['uvindex']),
                    'clouds': day["cloudcover"],
                    'pop': day['precipprob'],
                    'snow': day['snow'],
                    'sv': day['severerisk'],
                    'poptype': day['preciptype'],
                    'windspeed': day['windspeed'],
                    'winddir': trueDegree},
                "forecast": {
                    "basic": day['conditions'],
                    "details": day["description"],
                    "icon": day["icon"]}}
            returnWeek.append(returnDay)

    return returnWeek

def phrase7Build(day):

    beginPhrase = ""                                                                                                    ## BEGIN PHRASE ASSIGNMENT
    if day["daynum"] == 0:
        beginPhrase = uni.choose(
            [f"<break time = '0.5s'/> For {day['day']}, expect temperatures ranging around {day['temps']['day']}°**.",
             f"<break time = '0.5s'/> On {day['day']}, plan for temperatures around {day['temps']['day']}°**.",
             f"<break time = '0.5s'/> To begin my forecast, on {day['day']} I am predicting temps around {day['temps']['day']}°**."])
    elif 0 < day["daynum"] < 6:
        if day["daynum"] == 1:
            dayPhrase = "Secondly"
        elif day["daynum"] == 2:
            dayPhrase = "Thirdly"
        elif day["daynum"] == 3:
            dayPhrase = "Fourthly"
        elif day["daynum"] == 4:
            dayPhrase = "Fifthly"
        elif day["daynum"] == 5:
            dayPhrase = "Sixthly"
        beginPhrase = uni.choose([
            f"<break time = '0.5s'/> In addition, on {day['day']}, anticipate temperatures to average at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> {dayPhrase}, for {day['day']}, plan on temperatures being around {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> As for {day['day']}, expect temperatures to linger at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> On {day['day']}, I'm seeing temperatures at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> And as for {day['day']}, I am forecasting temperatures around {day['temps']['day']}°**."])
    elif day["daynum"] == 6:
        beginPhrase = uni.choose([
            f"<break time = '0.75s'/> And lastly, {day['day']}, expect temperatures to range around {day['temps']['day']}°**",
            f"<break time = '0.75s'/> And as for {day['day']}, I forecast temperatures to be averaging {day['temps']['day']}°**.",
            f"<break time = '0.75s'/> And for our last day, On {day['day']}, I predict temperatures at {day['temps']['day']}°**"])

    difference = day['temps']['day'] - day['temps']['fl']
    if difference > 2 or difference < -2:
        beginPhrase = beginPhrase.replace("**", uni.choose[
            f" with it feeling like {day['temps']['fl']}°",
            f". The average feels-like temperature is {day['temps']['fl']}°",
            f" and feels-like temperatures around {day['temps']['fl']}°",
            f" and it will feel around {day['temps']['fl']}° outside",
            f" with feels like averaging {day['temps']['fl']}°",
            f" with feels like following at {day['temps']['fl']}°.",
            f" with feels like doing the same at {day['temps']['fl']}°.",
        ])
    else:
        beginPhrase = beginPhrase.replace("**", "")
    beginPhrase += uni.choose([" I am forecasting it to be ", " Expect it to be ", \
        " Seems like it will be ", " Anticipate it being ", 
        " The forecast shows it as ", " Seems like the forecasting is showing it to be "])
    
    beginPhrase += day['forecast']['details']

    importantPhrase = ""
    if "ice" in day["important"]:
        importantPhrase += uni.choose([
            "Additionally, there will be a pretty high chance of ice. Drive safe",
            "I want to warn you of the ice danger. Please drive safe.",
            "There seems to be an ice danger. Please drive safe."])
    if "snow" in day["important"]:
        if day["important"]["snow"] == "expected" or day["important"]["snow"] == "probable":
            importantPhrase += uni.choose([
                "Enjoy the expected snow.",
                "Drive safe in the snow.",
                "I anticipate snow-men and snow-women in your future.",
                "I wonder how fast the snow will melt this time."])
        elif day["important"]["snow"] == "chance":
            importantPhrase += uni.choose([
                "There seems to be a chance of snow in the forecast.",
                "I see a small chance of snow in the forecast.",
                "I anticipate small snow-men and snow-women in your future.",
                "I see a small chance of snow. I wonder how fast the snow will melt this time."])
    if "severe" in day["important"]:
        if day["important"]["severe"] == "severe":
            importantPhrase += uni.choose([
                "There is a very high chance of severe weather forecasted.",
                "I am noticing a very high chance of severe weather.",
                "The forecast shows a very high chance of severe weather.",])

    notesPhrase = ""
    if "fronts" in day["notes"]:
        if day["notes"]["fronts"] == "warm front":
            notesPhrase += uni.choose([
                "I've noticed that there's a warm front moving in at this point.",
                "Seems like a warm front is beginning to enter the area at this point in the forecast",
                "I see a possibility of a warm front moving into the area."])
        if day["notes"]["fronts"] == "cold front":
            notesPhrase += uni.choose([
                "I've noticed that a cold front is moving in around this point in the forecast.",
                "The wind directions suggest a cold front could be moving in.",
                "I've noticed the possbility of a cold front entering the area based on the wind changes."])
        if day["notes"]["fronts"] == "conclusive wf":
            notesPhrase += uni.choose([
                "I've noticed that the weather data suggests a warm front is beginning to enter the area.",
                "Based on the forecast, it seems like the area is under the influence of a warm front.",
                "The southerly winds and higher barometric pressure suggest a warm front moving."])
        if day['notes']['fronts'] == "conclusive cf":
            notesPhrase += uni.choose([
                "The weather data suggest that a cold front is beginning to enter the area.",
                "I've noticed a possibility of a cold front entering the area based on the wind changes and lower barometric pressures.",
                "I've observed the possibility of a cold front moving in around this week.'"
            ])
    returnPhrase = beginPhrase + " " + importantPhrase + " " + notesPhrase
    
    return returnPhrase

def forecast7Init(forecastUpdate):
    procweek = data7Process()
    week = {
        "dt": datetime.datetime.now(),
        "weather": procweek}                                ## Convert to dict with weather = procweek and dt = now

    if forecastUpdate:                          ## Universal Variable Hour Weather Update
        if universal.weather['past7week']:
            weekTime = universal.weather['past7week']['dt']
            if (weekTime + 604800) <= week['dt']:
                universal.weather['past7week'] = week
        else:
            universal.weather['past7week'] = week
        universal.weather['7week'] = week

    windDirections = []
    weekPhrase = ""
    weeklyTemp = 0
    weeklyFlTemp = 0
    for day in procweek:
        print("\n")
        print(repr(day))
    for day in procweek:
        if procweek[procweek.index(day)-1]:
            ref = procweek[procweek.index(day)-1]
            main = procweek[procweek.index(day)]
            main['trend'] = {}
            main['important'] = {}
            main['notes'] = {}
            if (main['details']['pressure']-2) > ref['details']['pressure']:          # Pressure Trend Check
                main['trend']['pressure'] = "rising"
                resultContext = 'good'
            elif (ref['details']['pressure']-2) > main['details']['pressure']:
                main['trend']['pressure'] = "lowering"
            if (main['details']['humidity']-10) > ref['details']['humidity']:          # Humidity Trend Check
                main['trend']['humidity'] = "rising"
            elif (ref['details']['humidity']-10) > main['details']['humidity']:
                main['trend']['humidity'] = "lowering"
            if main['details']['sv'] > 30:                                # Severe Weather Important Check
                main['important']['severe'] = "moderate"
                resultContext = 'bad'
            if main['details']['sv'] > 60:
                main['important']['severe'] = 'high'
                resultContext = 'bad'
            if main['details']['sv'] > 80:
                main['important']['severe'] = 'severe'
                resultContext = 'bad'
            if main['details']['uvi'] > 8:                               # High UV Index Important Check
                main['important']['uvi'] = 'high'
                resultContext = 'good'

            windDirections.append(main['details']['winddir'])            # Wind direction and Front Notes Check
            n = 0
            s = 0
            w = 0
            e = 0

            for direction in windDirections:
                if direction == "N" or direction == "NW" or direction == "NE":
                    n+=1
                if direction == "S" or direction == "SE" or direction == "SW":
                    s+=1
                if direction == "E" or direction == "SE" or direction == "NE":
                    e+=1
                if direction == "W" or direction == "NW" or direction == "SW":
                    w+=1

            if len(windDirections) > 2 and "firstcheck" not in windDirections:
                if ((w > 1 and n > 1) or (e > 1 and n > 1) or n > 2) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 1 and s > 1) or (e > 1 and s > 1) or s > 2) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 7:
                if ((w > 3 and n > 3) or (e > 3 and n > 3) or n > 3) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 3 and s > 3) or (e > 3 and s > 3) or s > 3) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                else:
                    average = 0
                    for day in procweek:
                        average = day['details']['pressure']
                    average = average / 7
                    if average >= 1015 and s>2:
                        main['notes']['fronts'] = "conclusive wf"
                    elif average <=1014 and n>2:
                        main['notes']['fronts'] = "conclusive cf"

                                                                         # Snow and Ice Important Check

            if main["details"]["snow"] > 0 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "chance"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "probable"
            if main["details"]["snow"] > 70 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "expected"

            if type(main['details']['poptype']) is list and ("freezingrain" in main['details']['poptype'] or "ice" in main['details']['poptype']):
                main['important']['ice'] = "expected"
                resultContext = "bad"
        else: 
            main = procweek[procweek.index(day)]
            main['trend'] = {}
            main['important'] = {}
            main['notes'] = {}

            if main['details']['sv'] > 30:                                # Severe Weather Important Check
                main['important']['severe'] = "moderate"
                resultContext = 'bad'
            if main['details']['sv'] > 60:
                main['important']['severe'] = 'high'
                resultContext = 'bad'
            if main['details']['sv'] > 80:
                main['important']['severe'] = 'severe'
                resultContext = 'bad'
            if main['details']['uvi'] > 8:                               # High UV Index Important Check
                main['important']['uvi'] = 'high'
                resultContext = 'good'

            windDirections.append(main['details']['winddir'])            # Wind direction and Front Notes Check
            n = 0
            s = 0
            w = 0
            e = 0

            for direction in windDirections:
                if direction == "N" or direction == "NW" or direction == "NE":
                    n+=1
                if direction == "S" or direction == "SE" or direction == "SW":
                    s+=1
                if direction == "E" or direction == "SE" or direction == "NE":
                    e+=1
                if direction == "W" or direction == "NW" or direction == "SW":
                    w+=1

            if len(windDirections) > 2 and "firstcheck" not in windDirections:
                if ((w > 1 and n > 1) or (e > 1 and n > 1) or n > 2) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 1 and s > 1) or (e > 1 and s > 1) or s > 2) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 7:
                if ((w > 3 and n > 3) or (e > 3 and n > 3) or n > 3) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 3 and s > 3) or (e > 3 and s > 3) or s > 3) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                else:
                    average = 0
                    for day in procweek:
                        average = day['details']['pressure']
                    average = average / 7
                    if average >= 1015 and s>2:
                        main['notes']['fronts'] = "conclusive wf"
                    elif average <=1014 and n>2:
                        main['notes']['fronts'] = "conclusive cf"
                                                                         # Snow and Ice Important Check

            if main["details"]["snow"] > 0 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "chance"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "probable"
            if main["details"]["snow"] > 70 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "expected"

            if type(main['details']['poptype']) is list and ("freezingrain" in main['details']['poptype'] or "ice" in main['details']['poptype']):
                main['important']['ice'] = "expected"
                resultContext = "bad"
        
        weeklyTemp += day['temps']['day']
        weeklyFlTemp += day['temps']['fl']

        phrase = phrase7Build(procweek[procweek.index(day)])
        procweek[procweek.index(day)]['phrase'] = phrase
        weekPhrase += phrase + " "

    if not resultContext:
        resultContext = "good"
    
    temperature = ""

    if weeklyTemp < 20 or weeklyFlTemp < 20:
        temperature = "frosty"
    elif weeklyTemp < 32 or weeklyFlTemp < 32:
        temperature = "chilly"
    elif weeklyTemp < 50 or weeklyFlTemp < 50:
        temperature = "mild"
    elif weeklyTemp < 80 or weeklyFlTemp < 80:
        temperature = "warm"
    elif weeklyTemp < 100 or weeklyFlTemp < 100:
        temperature = "hot"
    elif weeklyFlTemp > 100 or weeklyFlTemp > 100:
        temperature = "scorching"

    intro = uni.choose([
        f"For your {temperature} seven day forecast, I am seeing a trend of ",
        f"For your {temperature} seven-day forecast this week, I am noticing ",
        f"The {temperature} forecast this week shows a trend of ",
        "For this forecast, I am noticing a trend of ",
        "Seems like this week, "
    ])
    
    weekPhrase = intro + weeklyDataJSON["description"] + " " + weekPhrase

    return weekPhrase

    
def data5Process():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day1 = weeklyDataJSON['days'][1]
    day2 = weeklyDataJSON['days'][2]
    day3 = weeklyDataJSON['days'][3]
    day4 = weeklyDataJSON['days'][4]
    day5 = weeklyDataJSON['days'][5]
    day6 = weeklyDataJSON['days'][6]
    day5 = weeklyDataJSON['days'][5]
    week = [day1, day2, day3, day4, day5, day6, day5]
    returnWeek = []
    for day in week:
        if 'zizdent' not in day:
            dayName = unitconv.getDay(week.index(day))
            trueDegree = unitconv.degreeTranslate(day['winddir'])
            returnDay = {
                "zizdent":True,
                "day": dayName,
                "daynum": week.index(day),
                "temps": {
                    "day": round(day['temp']),
                    "fl": round(day['feelslike'])},
                "details": {
                    "pressure": round(day['pressure']),
                    'humidity': round(day['humidity']),
                    'dp': round(day['dew']),
                    'uvi': round(day['uvindex']),
                    'clouds': day["cloudcover"],
                    'pop': day['precipprob'],
                    'snow': day['snow'],
                    'sv': day['severerisk'],
                    'poptype': day['preciptype'],
                    'windspeed': day['windspeed'],
                    'winddir': trueDegree},
                "forecast": {
                    "basic": day['conditions'],
                    "details": day["description"],
                    "icon": day["icon"]}}
            returnWeek.append(returnDay)

    return returnWeek

def phrase5Build(day):

    beginPhrase = ""                                                                                                    ## BEGIN PHRASE ASSIGNMENT
    if day["daynum"] == 0:
        beginPhrase = uni.choose(
            [f"<break time = '0.5s'/> For {day['day']}, expect temperatures ranging around {day['temps']['day']}°**.",
             f"<break time = '0.5s'/> On {day['day']}, plan for temperatures around {day['temps']['day']}°**.",
             f"<break time = '0.5s'/> To begin my forecast, on {day['day']} I am predicting temps around {day['temps']['day']}°**."])
    elif 0 < day["daynum"] < 6:
        if day["daynum"] == 1:
            dayPhrase = "Secondly"
        elif day["daynum"] == 2:
            dayPhrase = "Thirdly"
        elif day["daynum"] == 3:
            dayPhrase = "Fourthly"
        elif day["daynum"] == 4:
            dayPhrase = "Fifthly"
        elif day["daynum"] == 5:
            dayPhrase = "Sixthly"
        beginPhrase = uni.choose([
            f"<break time = '0.5s'/> In addition, on {day['day']}, anticipate temperatures to average at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> {dayPhrase}, for {day['day']}, plan on temperatures being around {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> As for {day['day']}, expect temperatures to linger at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> On {day['day']}, I'm seeing temperatures at {day['temps']['day']}°**.",
            f"<break time = '0.5s'/> And as for {day['day']}, I am forecasting temperatures around {day['temps']['day']}°**."])
    elif day["daynum"] == 6:
        beginPhrase = uni.choose([
            f"<break time = '0.55s'/> And lastly, {day['day']}, expect temperatures to range around {day['temps']['day']}°**",
            f"<break time = '0.55s'/> And as for {day['day']}, I forecast temperatures to be averaging {day['temps']['day']}°**.",
            f"<break time = '0.55s'/> And for our last day, On {day['day']}, I predict temperatures at {day['temps']['day']}°**"])

    difference = day['temps']['day'] - day['temps']['fl']
    if difference > 2 or difference < -2:
        beginPhrase = beginPhrase.replace("**", uni.choose[
            f" with it feeling like {day['temps']['fl']}°",
            f". The average feels-like temperature is {day['temps']['fl']}°",
            f" and feels-like temperatures around {day['temps']['fl']}°",
            f" and it will feel around {day['temps']['fl']}° outside",
            f" with feels like averaging {day['temps']['fl']}°",
            f" with feels like following at {day['temps']['fl']}°.",
            f" with feels like doing the same at {day['temps']['fl']}°.",
        ])
    else:
        beginPhrase = beginPhrase.replace("**", "")
    beginPhrase += uni.choose([" I am forecasting it to be ", " Expect it to be ", \
        " Seems like it will be ", " Anticipate it being ", 
        " The forecast shows it as ", " Seems like the forecasting is showing it to be "])
    
    beginPhrase += day['forecast']['details']

    importantPhrase = ""
    if "ice" in day["important"]:
        importantPhrase += uni.choose([
            "Additionally, there will be a pretty high chance of ice. Drive safe",
            "I want to warn you of the ice danger. Please drive safe.",
            "There seems to be an ice danger. Please drive safe."])
    if "snow" in day["important"]:
        if day["important"]["snow"] == "expected" or day["important"]["snow"] == "probable":
            importantPhrase += uni.choose([
                "Enjoy the expected snow.",
                "Drive safe in the snow.",
                "I anticipate snow-men and snow-women in your future.",
                "I wonder how fast the snow will melt this time."])
        elif day["important"]["snow"] == "chance":
            importantPhrase += uni.choose([
                "There seems to be a chance of snow in the forecast.",
                "I see a small chance of snow in the forecast.",
                "I anticipate small snow-men and snow-women in your future.",
                "I see a small chance of snow. I wonder how fast the snow will melt this time."])
    if "severe" in day["important"]:
        if day["important"]["severe"] == "severe":
            importantPhrase += uni.choose([
                "There is a very high chance of severe weather forecasted.",
                "I am noticing a very high chance of severe weather.",
                "The forecast shows a very high chance of severe weather.",])

    notesPhrase = ""
    if "fronts" in day["notes"]:
        if day["notes"]["fronts"] == "warm front":
            notesPhrase += uni.choose([
                "I've noticed that there's a warm front moving in at this point.",
                "Seems like a warm front is beginning to enter the area at this point in the forecast",
                "I see a possibility of a warm front moving into the area."])
        if day["notes"]["fronts"] == "cold front":
            notesPhrase += uni.choose([
                "I've noticed that a cold front is moving in around this point in the forecast.",
                "The wind directions suggest a cold front could be moving in.",
                "I've noticed the possbility of a cold front entering the area based on the wind changes."])
        if day["notes"]["fronts"] == "conclusive wf":
            notesPhrase += uni.choose([
                "I've noticed that the weather data suggests a warm front is beginning to enter the area.",
                "Based on the forecast, it seems like the area is under the influence of a warm front.",
                "The southerly winds and higher barometric pressure suggest a warm front moving."])
        if day['notes']['fronts'] == "conclusive cf":
            notesPhrase += uni.choose([
                "The weather data suggest that a cold front is beginning to enter the area.",
                "I've noticed a possibility of a cold front entering the area based on the wind changes and lower barometric pressures.",
                "I've observed the possibility of a cold front moving in around this week.'"
            ])
    returnPhrase = beginPhrase + " " + importantPhrase + " " + notesPhrase
    
    return returnPhrase

def forecast5Init(forecastUpdate):
    procweek = data5Process()
    week = {
        "dt": datetime.datetime.now(),
        "weather": procweek}                                ## Convert to dict with weather = procweek and dt = now

    if forecastUpdate:                          ## Universal Variable Hour Weather Update
        if universal.weather['past5week']:
            weekTime = universal.weather['past5week']['dt']
            if (weekTime + 604800) <= week['dt']:
                universal.weather['past5week'] = week
        else:
            universal.weather['past5week'] = week
        universal.weather['5week'] = week

    windDirections = []
    weekPhrase = ""
    weeklyTemp = 0
    weeklyFlTemp = 0
    for day in procweek:
        print("\n")
        print(repr(day))
    for day in procweek:
        if procweek[procweek.index(day)-1]:
            ref = procweek[procweek.index(day)-1]
            main = procweek[procweek.index(day)]
            main['trend'] = {}
            main['important'] = {}
            main['notes'] = {}
            if (main['details']['pressure']-2) > ref['details']['pressure']:          # Pressure Trend Check
                main['trend']['pressure'] = "rising"
                resultContext = 'good'
            elif (ref['details']['pressure']-2) > main['details']['pressure']:
                main['trend']['pressure'] = "lowering"
            if (main['details']['humidity']-10) > ref['details']['humidity']:          # Humidity Trend Check
                main['trend']['humidity'] = "rising"
            elif (ref['details']['humidity']-10) > main['details']['humidity']:
                main['trend']['humidity'] = "lowering"
            if main['details']['sv'] > 30:                                # Severe Weather Important Check
                main['important']['severe'] = "moderate"
                resultContext = 'bad'
            if main['details']['sv'] > 60:
                main['important']['severe'] = 'high'
                resultContext = 'bad'
            if main['details']['sv'] > 80:
                main['important']['severe'] = 'severe'
                resultContext = 'bad'
            if main['details']['uvi'] > 8:                               # High UV Index Important Check
                main['important']['uvi'] = 'high'
                resultContext = 'good'

            windDirections.append(main['details']['winddir'])            # Wind direction and Front Notes Check
            n = 0
            s = 0
            w = 0
            e = 0

            for direction in windDirections:
                if direction == "N" or direction == "NW" or direction == "NE":
                    n+=1
                if direction == "S" or direction == "SE" or direction == "SW":
                    s+=1
                if direction == "E" or direction == "SE" or direction == "NE":
                    e+=1
                if direction == "W" or direction == "NW" or direction == "SW":
                    w+=1

            if len(windDirections) > 2 and "firstcheck" not in windDirections:
                if ((w > 1 and n > 1) or (e > 1 and n > 1) or n > 2) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 1 and s > 1) or (e > 1 and s > 1) or s > 2) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 5:
                if ((w > 3 and n > 3) or (e > 3 and n > 3) or n > 3) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 3 and s > 3) or (e > 3 and s > 3) or s > 3) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                else:
                    average = 0
                    for day in procweek:
                        average = day['details']['pressure']
                    average = average / 5
                    if average >= 1015 and s>2:
                        main['notes']['fronts'] = "conclusive wf"
                    elif average <=1014 and n>2:
                        main['notes']['fronts'] = "conclusive cf"

                                                                         # Snow and Ice Important Check

            if main["details"]["snow"] > 0 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "chance"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "probable"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "expected"

            if type(main['details']['poptype']) is list and ("freezingrain" in main['details']['poptype'] or "ice" in main['details']['poptype']):
                main['important']['ice'] = "expected"
                resultContext = "bad"
        else: 
            main = procweek[procweek.index(day)]
            main['trend'] = {}
            main['important'] = {}
            main['notes'] = {}

            if main['details']['sv'] > 30:                                # Severe Weather Important Check
                main['important']['severe'] = "moderate"
                resultContext = 'bad'
            if main['details']['sv'] > 60:
                main['important']['severe'] = 'high'
                resultContext = 'bad'
            if main['details']['sv'] > 80:
                main['important']['severe'] = 'severe'
                resultContext = 'bad'
            if main['details']['uvi'] > 8:                               # High UV Index Important Check
                main['important']['uvi'] = 'high'
                resultContext = 'good'

            windDirections.append(main['details']['winddir'])            # Wind direction and Front Notes Check
            n = 0
            s = 0
            w = 0
            e = 0

            for direction in windDirections:
                if direction == "N" or direction == "NW" or direction == "NE":
                    n+=1
                if direction == "S" or direction == "SE" or direction == "SW":
                    s+=1
                if direction == "E" or direction == "SE" or direction == "NE":
                    e+=1
                if direction == "W" or direction == "NW" or direction == "SW":
                    w+=1

            if len(windDirections) > 2 and "firstcheck" not in windDirections:
                if ((w > 1 and n > 1) or (e > 1 and n > 1) or n > 2) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 1 and s > 1) or (e > 1 and s > 1) or s > 2) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 5:
                if ((w > 3 and n > 3) or (e > 3 and n > 3) or n > 3) and main['details']['pressure'] <=1014:
                    main["notes"]["fronts"] = "cold front"
                elif ((w > 3 and s > 3) or (e > 3 and s > 3) or s > 3) and main['details']['pressure'] >=1016:
                    main["notes"]["fronts"] = "warm front"
                else:
                    average = 0
                    for day in procweek:
                        average = day['details']['pressure']
                    average = average / 5
                    if average >= 1015 and s>2:
                        main['notes']['fronts'] = "conclusive wf"
                    elif average <=1014 and n>2:
                        main['notes']['fronts'] = "conclusive cf"
                                                                         # Snow and Ice Important Check

            if main["details"]["snow"] > 0 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "chance"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "probable"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "expected"

            if type(main['details']['poptype']) is list and ("freezingrain" in main['details']['poptype'] or "ice" in main['details']['poptype']):
                main['important']['ice'] = "expected"
                resultContext = "bad"
        
        weeklyTemp += day['temps']['day']
        weeklyFlTemp += day['temps']['fl']

        phrase = phrase5Build(procweek[procweek.index(day)])
        procweek[procweek.index(day)]['phrase'] = phrase
        weekPhrase += phrase + " "

    if not resultContext:
        resultContext = "good"
    
    temperature = ""

    if weeklyTemp < 20 or weeklyFlTemp < 20:
        temperature = "frosty"
    elif weeklyTemp < 32 or weeklyFlTemp < 32:
        temperature = "chilly"
    elif weeklyTemp < 50 or weeklyFlTemp < 50:
        temperature = "mild"
    elif weeklyTemp < 80 or weeklyFlTemp < 80:
        temperature = "warm"
    elif weeklyTemp < 100 or weeklyFlTemp < 100:
        temperature = "hot"
    elif weeklyFlTemp > 100 or weeklyFlTemp > 100:
        temperature = "scorching"

    intro = uni.choose([
        f"For your {temperature} seven day forecast, I am seeing a trend of ",
        f"For your {temperature} seven-day forecast this week, I am noticing ",
        f"The {temperature} forecast this week shows a trend of ",
        "For this forecast, I am noticing a trend of ",
        "Seems like this week, "
    ])
    
    weekPhrase = intro + weeklyDataJSON["description"] + " " + weekPhrase

    return weekPhrase


def forecastDetail(info):
    detail = info['details']
    context = info['context']
    if 'data' in info:
        data = info['data']

    if context == "differentday":
        trueDay = data['day']
        if vars.weather['7week']:
            noResult = True
            for day in vars.weather['7week']:
                if 'day' in day:
                    if day == trueDay:
                        noResult = False
                        if detail == "temperatures":
                            return vars.weather['7week'][day]['temps']
                        elif detail == "pressure": 
                            return vars.weather['7week'][day]['details']['pressure']
                        elif detail == "humidity": 
                            return vars.weather['7week'][day]['details']['humidity']
                        elif detail == "dewpoint": 
                            return vars.weather['7week'][day]['details']['dp']
                        elif detail == "clouds": 
                            return vars.weather['7week'][day]['details']['clouds']
                        elif detail == "pop": 
                            return vars.weather['7week'][day]['details']['pop']
                        elif detail == "poptype": 
                            return vars.weather['7week'][day]['details']['poptype']
                        elif detail == "weather": 
                            return vars.weather['7week'][day]['forecast']
                        else:
                            noResult = True
            if noResult == True:
                days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                todayDay = uni.getDate("name")
                todayDay = days.index(todayDay)
                day = days.index(trueDay)
                difference = todayDay - day
                if difference > 0:
                    difference *= -1
                week = data7Process()
                day = week[day]
                if detail == "temperatures":
                    return day['temps']
                elif detail == "pressure": 
                    return day['details']['pressure']
                elif detail == "humidity": 
                    return day['details']['humidity']
                elif detail == "dewpoint": 
                    return day['details']['dp']
                elif detail == "clouds": 
                    return day['details']['clouds']
                elif detail == "pop": 
                    return day['details']['pop']
                elif detail == "poptype": 
                    return day['details']['poptype']
                elif detail == "weather": 
                    return day['forecast']                
    elif context == "today": 
        day = dataProcess()
        if detail == "temperatures":
            return day['temps']
        elif detail == "pressure": 
            return day['details']['pressure']
        elif detail == "humidity": 
            return day['details']['humidity']
        elif detail == "dewpoint": 
            return day['details']['dp']
        elif detail == "clouds": 
            return day['details']['clouds']
        elif detail == "pop": 
            return day['details']['pop']
        elif detail == "poptype": 
            return day['details']['poptype']
        elif detail == "weather": 
            return day['forecast']  

def forecast(forecastType="day", forecastUpdate=True, justUpdate=False, detail=False):
    if forecastType == "7day":
        result = forecast7Init(forecastUpdate)
        if result:
            return result
    elif forecastType == "5day":
        result = forecast5Init(forecastUpdate)
        if result:
            return result
    elif forecastType == "today":
        result = forecastInit(forecastUpdate)
        if result:
            return result
    elif forecastType == "tomorrow":
        result = forecastTomInit(False)
        if result:
            return result
    elif forecastType == "detail":
        result = forecastDetail(detail)
        if result:
            return result


def update(updateType):
    pass





