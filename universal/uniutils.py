import requests
import random 
from universal import vars
from universal import speechhandle
from universal import synonyms
import re
clientid = ""

def choose(phrases):
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase = random.choice(phrases)
    return phrase



def checkforSyn(string):
    for x in range(0,10):
        for word in synonyms.synonyms:
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), string))
            if count >= 3:
                print("replacement")
                string = string.replace(word, choose(synonyms.synonyms[word]), random.randrange(1,4))
        for word in synonyms.wordReplacement:
            choice = random.choice([True, False, True])
            if choice:
                string = string.replace(word, choose(synonyms.wordReplacement[word]))
    print(string)
    return string
    
def speak(sentence):
    print(sentence)
    sentence = checkforSyn(sentence)
    print(sentence)
    sentence = "<speak> " + sentence + " </speak>"
    speechhandle.process(sentence)
    vars.phrases['pastPhrases'].insert(0, vars.phrases['lastPhrase'])
    if len(vars.phrases['pastPhrases']) > vars.phrases['phraseLimit']:
        vars.phrases['pastPhrases'].pop(5)
    vars.phrases['lastPhrase'] = sentence

def conversation(keywords, literal):
    url = f"http://api.brainshop.ai/get?bid=160169&key=E4q6ThD41UgOQwvG&uid=nate&msg={literal}"

    response = requests.request("GET", url).json()
    speak(response['cnt'])
    return True

def makeContext(newContext):
    if vars.context['recentContext']:
        if vars.context['pastContext']:
            vars.context['pastContext'].append(vars.context['recentContext'])
        else:
            vars.context['pastContext'] = [vars.context['recentContext']]
        if len(vars.context['pastContext']) >= vars.context['pastContextMax']:
            vars.context['pastContext'].pop(len(vars.context['pastContext'])-1)

    vars.context['recentContext'] = newContext

    print(vars.context['recentContext'])
    print("success")