from weather import command as weatherkeys
from questions import command as questionkeys
from universal import vars as vari
from universal import uniutils as uni
import query



def analyze(keywords, question, type="direct"):
    question = question.split(" ")
    points = 0
    for word in keywords:
        for words in question:
            if word == words:
                points += 1
    if points > (len(keywords) * .74) or points > (len(question) * .74):
        if type=="direct":
            return True, None
        else:
            return points,question
    else:
        if type=="direct":
            return False, None
        else:
            return points,question      


def contextCheck(keys, literal):
    if vari.context['recentContext']:
        print("processing as context")
        context = vari.context['recentContext']
        keystoListen = context['data']['listenforkeys']
        success = False
        for keysListen in keystoListen:
            success = analyze(keys, keysListen)
            if success:
                success = context['data']['function'](keys, literal)
                if success: return True 
        if not success:
            if vari.context['pastContext']:
                for context in vari.context['pastContext']:
                    context = vari.context['recentContext']
                    keystoListen = context['data']['listenforkeys']
                    success = False
                    for keysListen in keystoListen:
                        success = analyze(keys, keysListen)
                        if success:
                            success = context['data']['function'](keys, literal)
                            if success: return True 
                    if success:
                        return True
        return False
    else: 
        return False


def process(keys, literal):
    if not query.vars['queryActive'] and not contextCheck(keys, literal):
        print("processing normal")
        weatherCands = []
        for key in weatherkeys.keys:
            success = analyze(keys,key)
            if success:
                weatherCands.append(key)
        questCands = []
        for key in questionkeys.keys:
            success = analyze(keys,key)
            if success:
                questCands.append(key)

        if len(weatherCands) > len(questCands):
            weatherkeys.process(keys, literal)
        elif len(questCands) > len(weatherCands):
            questionkeys.process(keys, literal)
        else:
            uni.speak(uni.choose([
                "I couldn't process that through my normal keyword detection. I am going to override my scoring and try again.",
                "I couldn't find an answer in my normal detection. I will override detection and try again.",
                "I couldn't find an answer under normal specification. I will override typical guidelines and try again."
            ]))
            bestGuess = 0 
            winner = ""
            for key in weatherkeys.keys:
                points,question = analyze(keys,key)
                if points > bestGuess:
                    bestGuess = points
                    winner = question + " weather"
            for key in questionkeys.keys:
                points,question = analyze(keys,key)
                if points > bestGuess:
                    bestGuess = points
                    winner = question + " question"
            
            if "weather" in winner:
                weatherkeys.process(keys, literal, override=True)
            elif "question" in winner:
                questionkeys.process(keys,literal,override=True)
            else:
                print("No result")
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
    #       }/