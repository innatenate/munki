import requests
from universal import uniutils as uni
from commands import speechtranslate as unitconv
import datetime
from universal import vars as universal
import calendar

weeklyData = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/2205%20West%20Canton%20Pl?unitGroup=us&key=BHFCCKY362XGLDYMK3FRKYZHB&include=obs%2Cfcst%2Cstats%2Chistfcst"
weeklyDataJSON = None

highPressureThresh = 1018
lowPressureThresh = 1013


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
            "detail": day["description"],
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
        f"Today's weather seems {context} with an average temperature of {day['temps']['day']}. Expect it to feel like {day['temps']['fl']}.",
        f"I'm forecasting a {context} day with temperatures around {day['temps']['day']}. The average feels-like temperature is {day['temps']['fl']}.",
        f"Today seems fairly {context} with temperatures around {day['temps']['day']} and feels-like temperatures around {day['temps']['fl']}.",
        f"I forecast today to be {context} with temperatures at {day['temps']['day']} and it will feel around {day['temps']['fl']} outside."
    ])

    weatherResult = uni.choose([
        f"I forecast it to be {day['forecast']['description']}.",
        f"You should expect {day['forecast']['description']}.",
        f"I am forecasting today to be {day['forecast']['description']}",
        f"For today, expect it to be {day['forecast']['description']}."
    ])
    mainPhrase = beginning + "<break time=3s/>" + important + "<break time=3s/>" + notes

    return mainPhrase 

def forecastInit(forecastUpdate, justUpdate):
    mainDay = dataProcess()
    pass

def dataTomProcess():
    pass
def phraseTomBuild():
    pass
def forecastTomInit():
    pass

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
    for day in week:
        if type(day) is not list:
            dayName = unitconv.getDay(week.index(day))
            trueDegree = unitconv.degreeTranslate(day['winddir'])
            returnDay = {
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
                    "detail": day["description"],
                    "icon": day["icon"]}}

            week.append(returnDay)
            week.remove(day)

    return week

def phrase7Build(day):

    beginPhrase = ""                                                                                                    ## BEGIN PHRASE ASSIGNMENT
    if day["daynum"] == 0:
        beginPhrase = uni.choose(
            [f"For {day['day']}, expect temperatures ranging around {day['temps']['day']}° with a feels like of {day['temps']['fl']}°.",
             f"On {day['day']}, plan for temperatures around {day['temps']['day']}° and a feels like of {day['temps']['fl']}°.",
             f"To begin my forecast, on {day['day']} I am predicting temps around {day['temps']['day']}° and feels like temps around {day['temps']['fl']}°."])
    elif 0 < day["daynum"] < 7:
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
            f"<break time = '2s'/> In addition, on {day['day']}, anticipate temperatures to average at {day['temps']['day']}° and feels like temperatures around {day['temps']['fl']}°.",
            f"<break time = '2s'/> {dayPhrase}, for {day['day']}, plan on temperatures being around {day['temps']['day']}° with feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> As for {day['day']}, expect temperatures to linger at {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '2s'/> On {day['day']}, I'm seeing temperatures at {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> And as for {day['day']}, I am forecasting temperatures around {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°."])
    elif day["daynum"] == 7:
        beginPhrase = uni.choose([
            f"<break time = '3s'/> And lastly, {day['day']}, expect temperatures to range around {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '3s'/> And as for {day['day']}, I forecast temperatures to be averaging {day['temps']['day']}° with feels like averaging {day['temps']['fl']}°.",
            f"<break time = '3s'/> And for our last day, On {day['day']}, I predict temperatures at {day['temps']['day']}° with feels like following at {day['temps']['fl']}°."])

    beginPhrase += uni.choose(["<break time = '2s'/>  I am forecasting it to be ", "<break time = '2s'/>  Expect it to be ", \
        "<break time = '2s'/>  Seems like it will be ", "<break time = '2s'/>  Anticipate it being ", 
        "<break time = '2s'/>  The forecast shows it as ", "<break time = '2s'/> Seems like the forecasting is showing it to be "])
    
    beginPhrase += day['forecast']['description']

    importantPhrase = ""
    if "ice" in day["important"]:
        importantPhrase += uni.choose([
            "<break time = '2s'/> Additionally, there will be a pretty high chance of ice. Drive safe",
            "<break time = '2s'/>I want to warn you of the ice danger. Please drive safe.",
            "<break time = '2s'/>There seems to be an ice danger. Please drive safe."])
    if "snow" in day["important"]:
        if day["important"]["snow"] == "expected" or day["important"]["snow"] == "probable":
            importantPhrase += uni.choose([
                "<break time = '2s'/> Enjoy the expected snow.",
                "<break time = '2s'/> Drive safe in the snow.",
                "<break time = '2s'/> I anticipate snow-men and snow-women in your future.",
                "<break time = '2s'/> I wonder how fast the snow will melt this time."])
        elif day["important"]["snow"] == "chance":
            importantPhrase += uni.choose([
                "<break time = '2s'/> There seems to be a chance of snow in the forecast.",
                "<break time = '2s'/> I see a small chance of snow in the forecast.",
                "<break time = '2s'/> I anticipate small snow-men and snow-women in your future.",
                "<break time = '2s'/> I see a small chance of snow. I wonder how fast the snow will melt this time."])
    if "severe" in day["important"]:
        if day["important"]["severe"] == "severe":
            importantPhrase += uni.choose([
                "<break time = '2s'/> There is a very high chance of severe weather forecasted.",
                "<break time = '2s'/> I am noticing a very high chance of severe weather.",
                "<break time = '2s'/> The forecast shows a very high chance of severe weather.",])

    notesPhrase = ""
    if "fronts" in day["notes"]:
        if day["notes"]["fronts"] == "warm front":
            notesPhrase += uni.choose([
                "<break time = '2s'/> I've noticed that there's a warm front moving in at this point.",
                "<break time = '2s'/> Seems like a warm front is beginning to enter the area at this point in the forecast",
                "<break time = '2s'/> I see a possibility of a warm front moving into the area."])
        if day["notes"]["fronts"] == "cold front":
            notesPhrase += uni.choose([
                "<break time = '2s'/> I've noticed that a cold front is moving in around this point in the forecast.",
                "<break time = '2s'/> The wind directions suggest a cold front could be moving in.",
                "<break time = '2s'/> I've noticed the possbility of a cold front entering the area based on the wind changes."])
        if day["notes"]["fronts"] == "sporadic":
            notesPhrase += uni.choose([
                "<break time = '2s'/> The atmopspheric pressure seems to be pretty sporadic at this point. That could suggest potential rain.",
                "<break time = '2s'/> The atmopshere seems pretty sporadic at this point. That could lead to sporadic weather as well.",
                "<break time = '2s'/> I've noticed a lot of differences in the atmopshere throughout the week. That could lead to sporadic weather."])

    returnPhrase = beginPhrase + " " + importantPhrase + " " + notesPhrase
    
    return returnPhrase

def forecast7Init(forecastUpdate):
    procweek = data7Process()
    week = {
        "dt": datetime.datetime.now(),
        "weather": procweek}                                ## Convert to dict with weather = procweek and dt = now

    if forecastUpdate:                          ## Universal Variable Hour Weather Update
        if universal.weather['pastweek']:
            weekTime = universal.weather['pastweek']['dt']
            if (weekTime + 604800) <= week['dt']:
                universal.weather['pastweek'] = week
        else:
            universal.weather['pastweek'] = week
        universal.weather['currentweek'] = week

    windDirections = []
    weekPhrase = ""
    weeklyTemp = 0
    weeklyFlTemp = 0

    for day in procweek:
        if procweek[procweek.index(day)-1]:
            ref = procweek[procweek.index(day)-1]
            main = procweek[day]
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
                if (w > 1 and n > 1) or (e > 1 and n > 1) or n > 2:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 1 and s > 1) or (e > 1 and s > 1) or s > 2:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 7:
                if (w > 3 and n > 3) or (e > 3 and n > 3) or n > 3:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 3 and s > 3) or (e > 3 and s > 3) or s > 3:
                    main["notes"]["fronts"] = "warm front"
                else:
                    main["notes"]["fronts"] = "sporadic"
                    resultContext = "bad"

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
            main = procweek[day]
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
                if (w > 1 and n > 1) or (e > 1 and n > 1) or n > 2:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 1 and s > 1) or (e > 1 and s > 1) or s > 2:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 7:
                if (w > 3 and n > 3) or (e > 3 and n > 3) or n > 3:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 3 and s > 3) or (e > 3 and s > 3) or s > 3:
                    main["notes"]["fronts"] = "warm front"
                else:
                    main["notes"]["fronts"] = "sporadic"
                    resultContext = "bad"

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

        phrase = phrase7Build(procweek[day])
        procweek[day]['phrase'] = phrase
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

    uni.makeContext("sevendayforecast",True,resultContext, passedData=weekPhrase)
    return weekPhrase


def data5Process():
    global weeklyDataJSON
    weeklyDataJSON = requests.get(weeklyData).json()
    day1 = weeklyDataJSON['days'][1]
    day2 = weeklyDataJSON['days'][2]
    day3 = weeklyDataJSON['days'][3]
    day4 = weeklyDataJSON['days'][4]
    day5 = weeklyDataJSON['days'][5]
    week = [day1, day2, day3, day4, day5]
    for day in week:
        if type(day) is not list:
            dayName = unitconv.getDay(week.index(day))
            trueDegree = unitconv.degreeTranslate(day['winddir'])
            returnDay = {
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
                    "detail": day["description"],
                    "icon": day["icon"]}}

            week.append(returnDay)
            week.remove(day)

    return week

def phrase5Build(day):

    beginPhrase = ""                                                                                                    ## BEGIN PHRASE ASSIGNMENT
    if day["daynum"] == 0:
        beginPhrase = uni.choose(
            [f"For {day['day']}, expect temperatures ranging around {day['temps']['day']}° with a feels like of {day['temps']['fl']}°.",
             f"On {day['day']}, plan for temperatures around {day['temps']['day']}° and a feels like of {day['temps']['fl']}°.",
             f"To begin my forecast, on {day['day']} I am predicting temps around {day['temps']['day']}° and feels like temps around {day['temps']['fl']}°."])
    elif 0 < day["daynum"] < 5:
        if day["daynum"] == 1:
            dayPhrase = "Secondly"
        elif day["daynum"] == 2:
            dayPhrase = "Thirdly"
        elif day["daynum"] == 3:
            dayPhrase = "Fourthly"
        beginPhrase = uni.choose([
            f"<break time = '2s'/> In addition, on {day['day']}, anticipate temperatures to average at {day['temps']['day']}° and feels like temperatures around {day['temps']['fl']}°.",
            f"<break time = '2s'/> {dayPhrase}, for {day['day']}, plan on temperatures being around {day['temps']['day']}° with feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> As for {day['day']}, expect temperatures to linger at {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '2s'/> On {day['day']}, I'm seeing temperatures at {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> And as for {day['day']}, I am forecasting temperatures around {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°."])
    elif day["daynum"] == 5:
        beginPhrase = uni.choose([
            f"<break time = '3s'/> And lastly, {day['day']}, expect temperatures to range around {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '3s'/> And as for {day['day']}, I forecast temperatures to be averaging {day['temps']['day']}° with feels like averaging {day['temps']['fl']}°.",
            f"<break time = '3s'/> And for our last day, On {day['day']}, I predict temperatures at {day['temps']['day']}° with feels like following at {day['temps']['fl']}°."])

    beginPhrase += uni.choose(["<break time = '2s'/>  I am forecasting it to be ", "<break time = '2s'/>  Expect it to be ", \
        "<break time = '2s'/>  Seems like it will be ", "<break time = '2s'/>  Anticipate it being ", 
        "<break time = '2s'/>  The forecast shows it as ", "<break time = '2s'/> Seems like the forecasting is showing it to be "])
    
    beginPhrase += day['forecast']['description']

    importantPhrase = ""
    if "ice" in day["important"]:
        importantPhrase += uni.choose([
            "<break time = '2s'/> Additionally, there will be a pretty high chance of ice. Drive safe",
            "<break time = '2s'/>I want to warn you of the ice danger. Please drive safe.",
            "<break time = '2s'/>There seems to be an ice danger. Please drive safe."])
    if "snow" in day["important"]:
        if day["important"]["snow"] == "expected" or day["important"]["snow"] == "probable":
            importantPhrase += uni.choose([
                "<break time = '2s'/> Enjoy the expected snow.",
                "<break time = '2s'/> Drive safe in the snow.",
                "<break time = '2s'/> I anticipate snow-men and snow-women in your future.",
                "<break time = '2s'/> I wonder how fast the snow will melt this time."])
        elif day["important"]["snow"] == "chance":
            importantPhrase += uni.choose([
                "<break time = '2s'/> There seems to be a chance of snow in the forecast.",
                "<break time = '2s'/> I see a small chance of snow in the forecast.",
                "<break time = '2s'/> I anticipate small snow-men and snow-women in your future.",
                "<break time = '2s'/> I see a small chance of snow. I wonder how fast the snow will melt this time."])
    if "severe" in day["important"]:
        if day["important"]["severe"] == "severe":
            importantPhrase += uni.choose([
                "<break time = '2s'/> There is a very high chance of severe weather forecasted.",
                "<break time = '2s'/> I am noticing a very high chance of severe weather.",
                "<break time = '2s'/> The forecast shows a very high chance of severe weather.",])

    notesPhrase = ""
    if "fronts" in day["notes"]:
        if day["notes"]["fronts"] == "warm front":
            notesPhrase += uni.choose([
                "<break time = '2s'/> I've noticed that there's a warm front moving in at this point.",
                "<break time = '2s'/> Seems like a warm front is beginning to enter the area at this point in the forecast",
                "<break time = '2s'/> I see a possibility of a warm front moving into the area."])
        if day["notes"]["fronts"] == "cold front":
            notesPhrase += uni.choose([
                "<break time = '2s'/> I've noticed that a cold front is moving in around this point in the forecast.",
                "<break time = '2s'/> The wind directions suggest a cold front could be moving in.",
                "<break time = '2s'/> I've noticed the possbility of a cold front entering the area based on the wind changes."])
        if day["notes"]["fronts"] == "sporadic":
            notesPhrase += uni.choose([
                "<break time = '2s'/> The atmopspheric pressure seems to be pretty sporadic at this point. That could suggest potential rain.",
                "<break time = '2s'/> The atmopshere seems pretty sporadic at this point. That could lead to sporadic weather as well.",
                "<break time = '2s'/> I've noticed a lot of differences in the atmopshere throughout the week. That could lead to sporadic weather."])

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
        universal.weather['current5week'] = week

    windDirections = []
    weekPhrase = ""
    weeklyTemp = 0
    weeklyFlTemp = 0

    for day in procweek:
        if procweek[procweek.index(day)-1]:
            ref = procweek[procweek.index(day)-1]
            main = procweek[day]
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
                if (w > 1 and n > 1) or (e > 1 and n > 1) or n > 2:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 1 and s > 1) or (e > 1 and s > 1) or s > 2:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 5:
                if (w > 3 and n > 3) or (e > 3 and n > 3) or n > 3:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 3 and s > 3) or (e > 3 and s > 3) or s > 3:
                    main["notes"]["fronts"] = "warm front"
                else:
                    main["notes"]["fronts"] = "sporadic"
                    resultContext = "bad"

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
            main = procweek[day]
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
                if (w > 1 and n > 1) or (e > 1 and n > 1) or n > 2:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 1 and s > 1) or (e > 1 and s > 1) or s > 2:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 5:
                if (w > 3 and n > 3) or (e > 3 and n > 3) or n > 3:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 3 and s > 3) or (e > 3 and s > 3) or s > 3:
                    main["notes"]["fronts"] = "warm front"
                else:
                    main["notes"]["fronts"] = "sporadic"
                    resultContext = "bad"

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

        phrase = phrase5Build(procweek[day])
        procweek[day]['phrase'] = phrase
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
        f"For your {temperature} five day forecast, I am seeing a trend of ",
        f"For your {temperature} five-day forecast this week, I am noticing ",
        f"The {temperature} forecast this week shows a trend of ",
        "For this forecast, I am noticing a trend of ",
        "Seems like this week, "
    ])
    
    weekPhrase = intro + weeklyDataJSON["description"] + " " + weekPhrase

    uni.makeContext("fivedayforecast",True,resultContext, passedData=weekPhrase)
    return weekPhrase



def forecast(forecastType="day", forecastUpdate=True, justUpdate=False):
    if forecastType == "7day":
        result = forecast7Init(forecastUpdate)
        if result:
            return result
    elif forecastType == "5day":
        result = forecast5Init(forecastUpdate)
        if result:
            return result
    elif forecastType == "day":
        result = forecastInit(forecastUpdate, justUpdate)
        if result:
            return result
    elif forecastType == "tomorrow":
        result = forecastTomInit()
        if result:
            return result


def update(updateType):
    pass





