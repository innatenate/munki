import requests
import random
from randfacts import get_fact
import time


keys = []
qb = {}

### Weather: Questionbank
###     'temp' :  Question
###             'keys'  :   ['what is the current temperature', 'what does it feel like outside', 'what is the temperature outside']
###             'function' : def func()    main']['pressure']} hectopascals, which is low from the average of 1025 hectopascals."])



qb['weatheroutside'] = {}
qb['weatheroutside']['keys'] = ["what weather today", "what weather outside" , "what's the current weather",
                                "what's the weather outside", "what does it feel like outside", "what is the weather today",
                                "What's today's weather", "what is weather outside currently"]
qb["weatheroutside"]['require'] = ["outside", "today", "weather", "today's", "current"]
qb["weatheroutside"]['whitelist'] = ["week"]
def weatherOutside(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['weatheroutside']['function'] = weatherOutside


qb['tempoutside'] = {}
qb['tempoutside']['keys'] = ["what is the high today", "what is the low today", "is it going to be hot today",
                             "is it hot outside today", "is it cold outside today", "should i wear a jacket today",
                             "is it going to be hot today", "is it going to be cold today"]
def tempOutside(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['tempoutside']['function'] = tempOutside


qb['raincheck'] = {}
qb['raincheck']['keys'] = ["do you think it will rain soon", "will it rain today", "is there a chance of rain today",
                           "will it precipitate today", "could it rain precipitate today", "raining today",
                           "is it going to rain today", "going rain soon today", "what is this precipitation chance"]
qb['raincheck']['require'] = ["rain", "precipitate", "raining"]
def rainCheck(keywords, info=False, info2=False, info3=False, info4=False): 
    pass
    return True
qb['raincheck']['function'] = rainCheck


qb['pressureoutside'] = {}
qb['pressureoutside']['keys'] = ["what atmosphere changes", "what atmosphere pressure", "what barometric pressure",
                                 "what is the atmospheric pressure"]
qb['pressureoutside']['require'] = ["barometric", "atmosphere", "atmospheric", "pressure"]
def pressureOutside(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['pressureoutside']['function'] = pressureOutside


qb['tomorrowcheck'] = {}
qb['tomorrowcheck']['keys'] = ["what is the weather tomorrow", "what is tomorrow's weather", "what is tomorrows weather"]
qb['tomorrowcheck']['require'] = ['tomorrow', "tomorrow's", "tomorrows"]
def tomorrowCheck(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['tomorrowcheck']['function'] = tomorrowCheck


qb['sevendaycheck'] = {}
qb['sevendaycheck']['keys'] = ["what is the seven day forecast", "what is it like this week", "what the 7-day forecast",
                               "what is the 7-day forecast this week", "what is the weather this week", "what's the weather this week",
                               "what is weekly forecast"]
qb['sevendaycheck']['require'] = ["week", "7-day", "seven", "week's", "weeks", "weekly"]
def sevenDayCheck(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['sevendaycheck']['function'] = sevenDayCheck


qb['fivedaycheck'] = {}
qb['fivedaycheck']['keys'] = ["what is the five day forecast", "what is it like this week", "what the five forecast",
                               "what is the 5-day forecast this week", "what is the weather this week", "what's the weather this week",
                               "what is weekly forecast"]
qb['fivedaycheck']['require'] = ["five", "5-day"]
def fiveDayCheck(keywords, info=False, info2=False, info3=False, info4=False):
    pass
    return True
qb['fivedaycheck']['function'] = fiveDayCheck



def process(keywords, info=False, info2=False, info3=False, info4=False):
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
                            if word in qb[question]['require']:
                                truePass = True
                        if truePass:
                            points += 1
                            if points > (len(keywords) * .74) or points > (len(phrase) * .74):
                                questionChoices.insert(0, [question, points])
                    else:
                        points += 1
                        if points > (len(keywords) * .74) or points > (len(phrase) * .74):
                            questionChoices.insert(0, [question, points])

    if len(questionChoices) > 0:
        largestNumber = 0

        for choice in questionChoices:
            if largestNumber < choice[1]:
                largestNumber = choice[1]

        debounce = False
        for choice in questionChoices:
            if choice[1] == largestNumber and not debounce:
                success = qb[choice[0]]['function'](keywords, info, info2, info3, info4)
                debounce = True

        if success:
            return True
        else:
            return False

    else:
        return False

for function in qb:
    for key in qb['function']['keys']:
        keys.append(key)
