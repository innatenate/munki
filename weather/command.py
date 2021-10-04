import requests
import random
from randfacts import get_fact
import time

from universal import uniutils as uni
from universal import vars
from weather import forecaster as fc

keys = []
qb = {}
day5 = None
day7 = None
tomorrowWeather = None
todayWeather = None
detailResult = None
contextResult = None
details = ["uv", "uv reading", "chance of rain", "chance of snow", "pressure", "barometric pressure", "atmospheric pressure", 
            "wind speed", "wind gust", "wind direction", "precipitation", "temperature", "temperatures", "feelslike", "feels like",
            "weather", "forecast", "detail", "details", "happening"]

days =  ["saturday", "sunday", "monday", "thursday", "friday", "wednesday", "tuesday"]

listeningKeys = []

for detail in details:
    for day in days:
        listeningKeys.append(f"what is the {detail} for {day}")
        listeningKeys.append(f"{detail} for {day}")
        listeningKeys.append(f"{detail} on {day}")
        listeningKeys.append(f"what is the {detail} on {day}")



### Weather: Questionbank
###     'temp' :  Question
###             'keys'  :   ['what is the current temperature', 'what does it feel like outside', 'what is the temperature outside']
###             'function' : def func()    main']['pressure']} hectopascals, which is low from the average of 1025 hectopascals."])



qb['weatheroutside'] = {}
qb['weatheroutside']['keys'] = ["what weather today", "what weather outside" , "what's the current weather",
                                "what's the weather outside", "what does it feel like outside", "what is the weather today",
                                "What's today's weather", "what is weather outside currently"]
qb["weatheroutside"]['require'] = ["outside", "today", "weather", "today's", "current"]
qb["weatheroutside"]['whitelist'] = ["week", "tomorrow"]
def weatherOutside(keywords, info=False, info2=False, info3=False, info4=False):
    phrase = fc.forecast(forecastType="today")
    uni.speak(phrase)
    return True
qb['weatheroutside']['function'] = weatherOutside
qb['weatheroutside']['context'] = {
           'context':  'weatheroutside',     # STR Name of context (ex in list)
           'dataProvided':   True,              # BOOL Was data provided
           'data': {                            # DICT Data if provided
               'takeaway': contextResult,              # STR Context takeaway (weather specific)
               'passedData': vars.weather['day'],          # OBJ Extra data if passed
               'listenfor': False,               # BOOL Check if listening for possible contextual requests
               'listenforkeys': None    # LIST List of keys for listening handler to listen for
               },
          }


qb['tempoutside'] = {}
qb['tempoutside']['keys'] = ["what is the high today", "what is the low today", "is it going to be hot today",
                             "is it hot outside today", "is it cold outside today", "should i wear a jacket today",
                             "is it going to be hot today", "is it going to be cold today"]
def tempOutside(keywords, info=False, info2=False, info3=False, info4=False):
    temperatures = fc.forecast(forecastType="detail", detail={'details':"temperatures", 'context':"today"})
    fl = temperatures['fl']
    main = temperatures['day']

    if fl < 0 or main < 0:
        context = uni.choose(["freezing", "wintry", "extremely cold", "painfully cold", "very cold"])
    elif fl < 32 or main < 32:
        context = uni.choose(["cold", "frosty", "icy", "crispy", "icy-cold"])
    elif fl < 50 or main < 50:
        context = uni.choose(["chilly", "cool", "brisk", "nippy"])
    elif fl < 70 or main < 70:
        context = uni.choose(["fair", "fresh", "refreshing", "vitalizing"])
    elif fl < 90 or (main < 90 and not fl > 100):
        context = uni.choose(["warm", "summery", "mild", "toasty", "hot", "balmy"])
    elif fl > 100 or main > 100:
        context = uni.choose(["scorching", "boiling", "borderline-tropical", "sweltering", "ovenlike", "torrid"])

    phrase = uni.choose([
        f"It seems {context} outside right now, with temperatures around {main}° and feels like around {fl}°.",
        f"It's {context} outsied right now. Temperatures are around {main}° and feels like around {fl}°.",
        f"Temperatures outside are expected around {main}° with a feels like of {fl}°. Expect it to be a {context} day.",
        f"Expect temperatures around {main}° and feels like around {fl}°."
    ])

    uni.speak(phrase)

    return True
qb['tempoutside']['function'] = tempOutside


qb['raincheck'] = {}
qb['raincheck']['keys'] = ["do you think it will rain soon", "will it rain today", "is there a chance of rain today",
                           "will it precipitate today", "could it rain precipitate today", "raining today",
                           "is it going to rain today", "going rain soon today", "what is this precipitation chance"]
qb['raincheck']['require'] = ["rain", "precipitate", "raining"]
def rainCheck(keywords, info=False, info2=False, info3=False, info4=False): 
    pop = fc.forecast(forecastType="detail", detail={'details':"pop", 'context':"today"})
    if pop > 10:
        phrase = uni.choose([
            "There is a small chance of precipitation today.",
            "It could rain today, but the chance is fairly low.",
            "There is a chance, but it is unlikely."])
        if pop > 25:
            popType = fc.forecast(forecastType="detail", detail={'details':"poptype", 'context':"today"})
            popType = popType[0]
            phrase = uni.choose([
                f"There is a chance of {popType} today, but is rather low.",
                f"There is a small possibility of {popType} today.",
                f"There is atleast a {pop}% chance of {popType} as of my current forecast."
            ])
            if pop > 50:
                phrase = uni.choose([
                    f"There is a {pop}% chance of {popType} as of my current forecast.",
                    f"I am currently forecasting a {pop}% chance of {popType}.",
                    f"I do see a chance of {popType} today. I am expecting at least a {pop}% chance."
                ])
    else:
        phrase = uni.choose([
            f'I do not see a chance of {uni.choose(["precipitation", "rain"])} today.',
            f'I dont see any form of {uni.choose(["precipitation", "rain"])} today.',
            f'I do not see a possibility of {uni.choose(["precipitation", "rain"])} today.',
            f'I am not currently forecasting any {uni.choose(["precipitation", "rain"])} today.'
        ])
    
    uni.speak(phrase)
    return True
qb['raincheck']['function'] = rainCheck


qb['pressureoutside']= {}
qb['pressureoutside']['keys'] = ["what atmosphere changes", "what atmosphere pressure", "what barometric pressure",
                                 "what is the atmospheric pressure"]
qb['pressureoutside']['require'] = ["barometric", "atmosphere", "atmospheric", "pressure"]
def pressureOutside(keywords, info=False, info2=False, info3=False, info4=False, direct=False):
    if not direct:
        pressure = fc.forecast(forecastType="detail", detail={'details':"pressure", 'context':"today"})
    else:
        pressure = direct['details']['pressure']
    if pressure < fc.lowPressureThresh:
        phrase = uni.choose([
            f"The -- {uni.choose(['barometric', 'atmospheric'])} pressure for the {uni.choose(['area', 'locale', 'location'])} ** is {pressure} hectopascals. That is a rather low reading.",
            f"{uni.choose(['barometric', 'atmospheric'])} pressure is reading at {pressure} for the area **. That reading is lower than the average for the {uni.choose(['area', 'locale'])}. "])
    elif pressure > fc.highPressureThresh:
        phrase = uni.choose([
            f"The -- {uni.choose(['barometric', 'atmospheric'])} pressure for the {uni.choose(['area', 'locale', 'location'])} ** is {pressure} hectopascals. That is a rather high reading.",
            f"{uni.choose(['barometric', 'atmospheric'])} pressure is reading at {pressure} for the area **. That reading is higher than the average for the {uni.choose(['area', 'locale'])}. "])
    else:
        phrase = uni.choose([
            f"The -- {uni.choose(['barometric', 'atmospheric'])} pressure for the {uni.choose(['area', 'locale', 'location'])} ** is {pressure} hectopascals.",
            f"{uni.choose(['barometric', 'atmospheric'])} pressure is reading at {pressure} for the area **."])

    if direct:
        phrase = phrase.replace("**", direct['day'])
        phrase = phrase.replace("--", "")
        return phrase
    else:
        phrase = phrase.replace("**", "")
        phrase = phrase.replace("--", "current")
        uni.speak(phrase)
        return True
qb['pressureoutside']['function'] = pressureOutside


qb['tomorrowcheck'] = {}
qb['tomorrowcheck']['keys'] = ["what is the weather tomorrow", "what is tomorrow's weather", "what is tomorrows weather"]
qb['tomorrowcheck']['require'] = ['tomorrow', "tomorrow's", "tomorrows"]
def tomorrowCheck(keywords, info=False, info2=False, info3=False, info4=False):
    phrase = fc.forecast(forecastType="tomorrow")
    global tomorrowWeather
    tomorrowWeather = phrase
    uni.speak(phrase)
    return True
qb['tomorrowcheck']['function'] = tomorrowCheck
qb['tomorrowcheck']['context'] = {
           'context':  'tomorrowcheck',     # STR Name of context (ex in list)
           'dataProvided':   True,              # BOOL Was data provided
           'data': {                            # DICT Data if provided
               'takeaway': contextResult,              # STR Context takeaway (weather specific)
               'passedData': vars.weather['pastDay'],          # OBJ Extra data if passed
               'listenfor': False,               # BOOL Check if listening for possible contextual requests
               'listenforkeys': None    # LIST List of keys for listening handler to listen for
               },
          }

qb['sevendaycheck'] = {}
qb['sevendaycheck']['keys'] = ["what is the seven day forecast", "what is it like this week", "what the 7-day forecast",
                               "what is the 7-day forecast this week", "what is the weather this week", "what's the weather this week",
                               "what is weekly forecast"]
qb['sevendaycheck']['require'] = ["week", "7-day", "seven", "week's", "weeks", "weekly"]
def sevenDayCheck(keywords, info=False, info2=False, info3=False, info4=False):
    phrase = fc.forecast(forecastType="7day")
    uni.speak(phrase)
    return True
qb['sevendaycheck']['function'] = sevenDayCheck
qb['sevendaycheck']['context'] = {
           'context':  'sevendaycheck',     # STR Name of context (ex in list)
           'dataProvided':   True,              # BOOL Was data provided
           'data': {                            # DICT Data if provided
               'takeaway': contextResult,              # STR Context takeaway (weather specific)
               'passedData': vars.weather['7week'],          # OBJ Extra data if passed
               'listenfor': True,               # BOOL Check if listening for possible contextual requests
               'listenforkeys': listeningKeys    # LIST List of keys for listening handler to listen for
               },
          }
def sevenDayContext(keywords, info=False, info2=False):
    print("processing context")
    for day in vars.weather['7week']['weather']:
        dayStr = day['day']
        print(dayStr)
        if dayStr.lower() in keywords:
            trueDay = day
            if "uvi" in keywords:
                uni.speak(uni.choose([
                    f"The UV reading for {trueDay['day']} is currently expected at {trueDay['details']['uvi']}.",
                    f"The UV reading for {trueDay['day']} is forecasted at {trueDay['details']['uvi']}.",
                    f"{trueDay['day']} is currenly expected to have a UV reading of {trueDay['details']['uvi']}."
                ]))
                return True
            elif "pressure" in keywords:
                success = pressureOutside(False, direct=trueDay)
                uni.speak(success)
                return True
            elif "wind" in keywords:
                if trueDay['details']['winddir']:
                    uni.speak(uni.choose([
                        f"The forecasted wind for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']}.",
                        f"Expect {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']} on {trueDay['day']}.",
                        f"The forecasted windspeeds for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']}.",
                    ]))
                    return True
                else:
                    uni.speak(uni.choose([
                        f"The forecasted wind for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph.",
                        f"Expect {trueDay['details']['windspeed']} mph.",
                        f"The forecasted windspeeds for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph.",
                    ]))
                    return True
            elif "temperatures" in keywords or "temps" in keywords or "temp" in keywords or "feelslike" in keywords or ("feels" in keywords and "link" in keywords):
                phrase = uni.choose([
                    f"The forecasted average temperature for {trueDay['day']} is expected at {trueDay['temps']['day']}°**.",
                    f"Expect an average of {trueDay['temps']['day']}°** on {trueDay['day']}.",
                    f"I am currently forecasting an average temperature of {trueDay['temps']['day']}°** on {trueDay['day']}."
                ])
                if trueDay['temps']['day'] == trueDay['temps']['fl']:
                    phrase = phrase.replace("**", "")
                else:
                    phrase = phrase.replace("**", uni.choose([
                        f" with an average feels like temp of {trueDay['temps']['fl']}°",
                        f" and a feels like temperature of {trueDay['temps']['fl']}°",
                    ]))
                uni.speak(phrase)
                return True
            elif "weather" in keywords or "details" in keywords or "forecast" in keywords or (("whats" in keywords or "what" in keywords) and "happening" in keywords):
                uni.speak(uni.choose([
                    f"Expect {trueDay['forecast']['basic']} on {trueDay['day']}.",
                    f"I am forecasting {trueDay['forecast']['basic']} {uni.choose(['for', 'on'])} {trueDay['day']}.",
                    f"For {trueDay['day']} my forecast reads, {trueDay['forecast']['details']}",
                ]))
                break
            elif "rain" in keywords or "precipitation" in keywords or "snow" in keywords or "ice" in keywords:
                if trueDay['details']['popType']:
                    uni.speak(uni.choose([
                        f"There is currently a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]}.",
                        f"For {trueDay['day']}, expect a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]}.",
                        f"I am forecasting a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]} on {trueDay['day']}."
                    ]))
                    return True
                else:
                    uni.speak(uni.choose([
                        f"I don't see a chance of rain or precipitation on {trueDay['day']}.",
                        f"I am not currently forecasting a chance of rain on {trueDay['day']}.",
                        f"I do not currently see any chance of {uni.choose(['precipitation', 'rain'])} on {trueDay['day']}."
                    ]))
                    return True
    print(keywords)
    return True
qb['sevendaycheck']['context']['data']['function'] = sevenDayContext


qb['fivedaycheck'] = {}
qb['fivedaycheck']['keys'] = ["what is the five day forecast", "what is it like this week", "what the five forecast",
                               "what is the 5-day forecast this week", "what is the weather this week", "what's the weather this week",
                               "what is weekly forecast"]
qb['fivedaycheck']['require'] = ["five", "5-day"]
def fiveDayCheck(keywords, info=False, info2=False, info3=False, info4=False):
    phrase = fc.forecast(forecastType="5day")
    uni.speak(phrase)
    return True
qb['fivedaycheck']['function'] = fiveDayCheck
qb['fivedaycheck']['context'] = {
           'context':  'fivedaycheck',     # STR Name of context (ex in list)
           'dataProvided':   True,              # BOOL Was data provided
           'data': {                            # DICT Data if provided
               'takeaway': contextResult,              # STR Context takeaway (weather specific)
               'passedData': vars.weather['5week'],          # OBJ Extra data if passed
               'listenfor': True,               # BOOL Check if listening for possible contextual requests
               'listenforkeys': listeningKeys    # LIST List of keys for listening handler to listen for
               },
          }
def fiveDayContext(keywords, info=False, info2=False):
    for day in vars.weather['5week']:
        if vars.weather['5week'][day]['day'].lower() in keywords:
            trueDay = vars.weather['5week'][day]
            details = ["uv", "uv reading", "chance of rain", "chance of snow", "pressure", "barometric pressure", "atmospheric pressure", 
            "wind speed", "wind gust", "wind direction", "precipitation", "temperature", "temperatures", "feelslike", "feels like",
            "weather", "forecast", "detail", "details", "happening"]
            if "uv" in keywords:
                uni.speak(uni.choose([
                    f"The UV reading for {trueDay['day']} is currently expected at {trueDay['details']['uv']}.",
                    f"The UV reading for {trueDay['day']} is forecasted at {trueDay['details']['uv']}.",
                    f"{trueDay['day']} is currenly expected to have a UV reading of {trueDay['details']['uv']}."
                ]))
                break
            elif "pressure" in keywords:
                success = pressureOutside(False, direct=trueDay)
                uni.speak(success)
            elif "wind" in keywords:
                if trueDay['details']['winddir']:
                    uni.speak(uni.choose([
                        f"The forecasted wind for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']}.",
                        f"Expect {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']} on {trueDay['day']}.",
                        f"The forecasted windspeeds for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph. {trueDay['details']['winddir']}.",
                    ]))
                    break
                else:
                    uni.speak(uni.choose([
                        f"The forecasted wind for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph.",
                        f"Expect {trueDay['details']['windspeed']} mph.",
                        f"The forecasted windspeeds for {trueDay['day']} is expected at {trueDay['details']['windspeed']} mph.",
                    ]))
                    break
            elif "temperatures" in keywords or "temperature" in keywords or "temps" in keywords or "temp" in keywords or "feelslike" in keywords or ("feels" in keywords and "link" in keywords):
                phrase = uni.choose([
                    f"The forecasted average temperature for {trueDay['day']} is expected at {trueDay['temps']['day']}°**.",
                    f"Expect an average of {trueDay['temps']['day']}°** on {trueDay['day']}.",
                    f"I am currently forecasting an average temperature of {trueDay['temps']['day']}°** on {trueDay['day']}."
                ])
                if trueDay['temps']['day'] == trueDay['temps']['fl']:
                    phrase.replace("**", "")
                else:
                    phrase.replace("**", uni.choose([
                        f" with an average feels like temp of {trueDay['temps']['fl']}°",
                        f" and a feels like temperature of {trueDay['temps']['fl']}°",
                    ]))
                uni.speak(phrase)
                break
            elif "weather" in keywords or "details" in keywords or "forecast" in keywords or (("whats" in keywords or "what" in keywords) and "happening" in keywords):
                uni.speak(uni.choose([
                    f"Expect {trueDay['forecast']['basic']} on {trueDay['day']}.",
                    f"I am forecasting {trueDay['forecast']['basic']} {uni.choose(['for', 'on'])} {trueDay['day']}.",
                    f"For {trueDay['day']} my forecast reads, {trueDay['forecast']['details']}",
                ]))
                break
            elif "rain" in keywords or "precipitation" in keywords or "snow" in keywords or "ice" in keywords:
                if trueDay['details']['popType']:
                    uni.speak(uni.choose([
                        f"There is currently a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]}.",
                        f"For {trueDay['day']}, expect a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]}.",
                        f"I am forecasting a {trueDay['details']['pop']}% chance of {trueDay['details']['popType'][0]} on {trueDay['day']}."
                    ]))
                    break
                else:
                    uni.speak(uni.choose([
                        f"I don't see a chance of rain or precipitation on {trueDay['day']}.",
                        f"I am not currently forecasting a chance of rain on {trueDay['day']}.",
                        f"I do not currently see any chance of {uni.choose(['precipitation', 'rain'])} on {trueDay['day']}."
                    ]))
                    break
    print(keywords)
    return True
qb['fivedaycheck']['context']['data']['function'] = fiveDayContext


def process(keywords, info=False, info2=False, info3=False, info4=False, override=False):
    questionChoices = []
    for question in qb:
        phrases = qb[question]['keys']
        for phrase in phrases:
            points = 0
            truePass = False
            phrase = phrase.split(" ")
            for pword in phrase:
                if pword in keywords:
                    if 'require' in qb[question]:
                        for word in keywords:
                            if 'whitelist' in qb[question]:
                                if word in qb[question]['whitelist']:
                                    points -= 100
                            if word in qb[question]['require']:
                                truePass = True
                        if truePass:
                            points += 1
                            if (points > (len(keywords) * .74) or points > (len(phrase) * .74)) or (override and points > (len(keywords) * 0.5)):
                                questionChoices.insert(0, [question, points])
                    else:
                        points += 1
                        if (points > (len(keywords) * .74) or points > (len(phrase) * .74)) or (override and points > (len(keywords) * 0.5)):
                            questionChoices.insert(0, [question, points])

    if len(questionChoices) > 0:
        largestNumber = 0

        for choice in questionChoices:
            if largestNumber < choice[1]:
                largestNumber = choice[1]

        debounce = False
        for choice in questionChoices:
            if choice[1] == largestNumber and not debounce:
                uni.makeContext(qb[choice[0]]['context'])
                success = qb[choice[0]]['function'](keywords, info, info2, info3, info4)
                debounce = True

        if success:
            return True
        else:
            return False

    else:
        return False

for function in qb:
    for key in qb[function]['keys']:
        keys.append(key)
