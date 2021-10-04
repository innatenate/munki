from weather import command as weatherkeys
from questions import command as questionkeys
from universal import vars as vari
from universal import uniutils as uni
import query



def analyze(keywords, question, type="direct", whitelist=[]):
    question = question.split(" ")
    points = 0
    for word in keywords:
        if word in whitelist:
            return False
        for words in question:
            if word == words and word not in whitelist:
                points += 1
    if points > (len(keywords) * .74) or points > (len(question) * .74):
        if type=="direct":
            return True, None
        elif type=="pointsandbool":
            return True, points, question
        else:
            return points,question
    else:
        if type=="direct":
            return False, None
        elif type=="pointsandbool":
            return False, points, question
        else:
            return points,question      


def contextCheck(keys, literal):
    if vari.context['recentContext']:
        if 'data' not in vari.context['recentContext']:
            return False
        elif vari.context['recentContext']['data'] == None:
            return False
        if 'listenfor' not in vari.context['recentContext']['data']:
            return False
        if not vari.context['recentContext']['data']['listenfor']:
            return False
        print("processing as context")
        context = vari.context['recentContext']
        keystoListen = context['data']['listenforkeys']
        success = False
        truesuccess = False
        for keysListen in keystoListen:
            if 'whitelist' in context['data']:
                success = analyze(keys, keysListen, whitelist=context['data']['whitelist'])
            else:
                success = analyze(keys, keysListen)
            if success:
                truesuccess = context['data']['function'](keys, literal)
                if truesuccess:  
                    print("tsuccess" + repr(truesuccess))
                    return True
        if not success:
            if vari.context['pastContext']:
                for context in vari.context['pastContext']:
                    context = vari.context['recentContext']
                    keystoListen = context['data']['listenforkeys']
                    truesuccess = False
                    success = False
                    for keysListen in keystoListen:
                        success = analyze(keys, keysListen)
                        if success:
                            print("success1" + success)
                            truesuccess = context['data']['function'](keys, literal)
                            if truesuccess: 
                                print("tsuccess1" + success)
                                return True 
                    if truesuccess:
                        return True
 
        print("susccess" + repr(success))
        print("trsuesuccess" + repr(truesuccess))
        if not success or not truesuccess:
            return False

    else: 
        return False


def process(keys, literal):
    res = contextCheck(keys, literal)
    print(res)
    if not query.vars['queryActive'] and not res:
        print("processing normal")
        weatherCands = []
        for key in weatherkeys.keys:
            success = analyze(keys,key)
            print("weather: " + repr(success))
            if success:
                weatherCands.append(key)
        questCands = []
        for key in questionkeys.keys:
            success = analyze(keys,key)
            print("question: " + repr(success))
            if success:
                questCands.append(key)
        print("Weather" + str(len(weatherCands)))
        print("questions" + str(len(questCands)))
        if len(weatherCands) > len(questCands):
            print("weather victor")
            attemptsuccess = weatherkeys.process(keys, literal)
        if len(questCands) > len(weatherCands) or not attemptsuccess:
            print("question victor")
            attemptsuccess = questionkeys.process(keys, literal)
        if not attemptsuccess:
            uni.conversation(keys, literal)
        #    uni.speak(uni.choose([
        #        "I couldn't process that through my normal keyword detection. I am going to override my scoring and try again.",
         #       "I couldn't find an answer in my normal detection. I will override detection and try again.",
   #             "I couldn't find an answer under normal specification. I will override typical guidelines and try again."
    #        ]))
     #       bestGuess = 0 
      #      winner = ""
      #      for key in weatherkeys.keys:
       #         points,question = analyze(keys,key)
       #         if points > bestGuess:
        #            bestGuess = points
       #            winner = question + " weather"
       #     for key in questionkeys.keys:
        #        points,question = analyze(keys,key)
        #        if points > bestGuess:
        #            bestGuess = points
        #            winner = question + " question"
         #   
        #    if "weather" in winner:
       #         weatherkeys.process(keys, literal, override=True)
       #     elif "question" in winner:
        #        questionkeys.process(keys,literal,override=True)
        #    else:
         #       print("No result")
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