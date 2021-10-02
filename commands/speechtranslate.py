from commands import keywordtranslate
import datetime
import calendar


def translate(words):
    trueWords = words
    words = words.lower()
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    words = ''.join(filter(whitelist.__contains__, words))
    words = words.split(" ")
    print(words)

    keywordtranslate.process(words, trueWords)


def degreeTranslate(degree):
    if (degree>337.5): return 'N'
    if (degree>292.5): return 'NW'
    if(degree>247.5): return 'W'
    if(degree>202.5): return 'SW'
    if(degree>157.5): return 'S'
    if(degree>122.5): return 'SE'
    if(degree>67.5): return 'E'
    if(degree>22.5): return 'NE'
    return 'N'


def kelvinConvert(value):
    return round(9 / 5 * ((int(value)) - 273) + 32)

def getDate(var):
    if var == "name":
        currentdate = datetime.date.today()
        currentdate = calendar.day_name[currentdate.weekday()]
        return currentdate

def getDay(num):
    currentdate = datetime.date.today()
    currentdate = calendar.day_name[currentdate.weekday()]
    if currentdate == "Monday":
        if num == 1:
            return "Tuesday"
        elif num == 2:
            return "Wednesday"
        elif num == 3:
            return "Thursday"
        elif num == 4:
            return "Friday"
        elif num == 5:
            return "Saturday"
        elif num == 6:
            return "Sunday"
        elif num == 7:
            return "Next Monday"
    elif currentdate == "Tuesday":
        if num == 7:
            return "Next Tuesday"
        elif num == 1:
            return "Wednesday"
        elif num == 2:
            return "Thursday"
        elif num == 3:
            return "Friday"
        elif num == 4:
            return "Saturday"
        elif num == 5:
            return "Sunday"
        elif num == 6:
            return "Monday"
    elif currentdate == "Wednesday":
        if num == 6:
            return "Tuesday"
        elif num == 7:
            return "Next Wednesday"
        elif num == 1:
            return "Thursday"
        elif num == 2:
            return "Friday"
        elif num == 3:
            return "Saturday"
        elif num == 4:
            return "Sunday"
        elif num == 5:
            return "Monday"
    elif currentdate == "Thursday":
        if num == 5:
            return "Tuesday"
        elif num == 6:
            return "Wednesday"
        elif num == 7:
            return "Next Thursday"
        elif num == 1:
            return "Friday"
        elif num == 2:
            return "Saturday"
        elif num == 3:
            return "Sunday"
        elif num == 4:
            return "Monday"
    elif currentdate == "Friday":
        if num == 4:
            return "Tuesday"
        elif num == 5:
            return "Wednesday"
        elif num == 6:
            return "Thursday"
        elif num == 7:
            return "Next Friday"
        elif num == 1:
            return "Saturday"
        elif num == 2:
            return "Sunday"
        elif num == 3:
            return "Monday"
    elif currentdate == "Saturday":
        if num == 3:
            return "Tuesday"
        elif num == 4:
            return "Wednesday"
        elif num == 5:
            return "Thursday"
        elif num == 6:
            return "Friday"
        elif num == 7:
            return "Next Saturday"
        elif num == 1:
            return "Sunday"
        elif num == 2:
            return "Monday"
    elif currentdate == "Sunday":
        if num == 2:
            return "Tuesday"
        elif num == 3:
            return "Wednesday"
        elif num == 4:
            return "Thursday"
        elif num == 5:
            return "Friday"
        elif num == 6:
            return "Saturday"
        elif num == 7:
            return "Next Sunday"
        elif num == 1:
            return "Monday"
