import time
from datetime import date, datetime
from weather import forecaster as forecast

context = {
    "recentContext" : None,
    "pastContext": None,
    "pastContextMax": 10

    #
    #                                   context dict example
    #   'recentcontext': {
    #       'context':  'asked7dayforecast',     # STR Name of context (ex in list)
    #       'dataProvided':   True,              # BOOL Was data provided
    #       'data': {                            # DICT Data if provided
    #           'takeaway': 'fair',              # STR Context takeaway (weather specific)
    #           'spokenstr': 'The seven-day...', # STR The spoken string if provided
    #           'passedData': forecast,          # OBJ Extra data if passed
    #           'listenfor': False               # BOOL Check if listening for possible contextual requests
    #           'listenforkeys': ["pressure"]    # LIST List of keys for listening handler to listen for
    #           },
    #       }
    #

}
weather = {
    'lastUpdate' : 0,
    'updateInterval': (60) * 60, #Change number in parenthesis to change minute
    '5week':None,
    'past5week':None,
    '7week':None,
    'past7week':None,
    'day':None,
    'pastDay':None,
    'current':None
}

phrases = {
    "lastPhrase": "None",
    'pastPhrases':[],
    'phraseLimit':5
}
#while time.sleep(weather['updateInterval']):
#    weather['lastUpdate'] = datetime.now()
#    weatherResult = forecast.update("all")