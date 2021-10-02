import random 
import vars


def choose(phrases):
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase = random.choice(phrases)
    return phrase

def makeContext(name, dataProvided=False, takeaway=False, spokenstr=False, passedData=False):
    context = {
        'context': name,
        'dataProvided': dataProvided,
        'data': {
            'takeaway': takeaway,
            'spokenstr': spokenstr,
            'passedData': passedData
        }
    }
    
    if vars.context['recentContext']:
        if vars.context['pastContext']:
            vars.context['pastContext'].append(vars.context['recentContext'])
        else:
            vars.context['pastContext'] = [vars.context['recentContext']]
        if len(vars.context['pastContext']) >= vars.context['pastContextMax']:
            vars.context['pastContext'].pop(len(vars.context['pastContext'])-1)
            
    vars.context['recentContext'] = context