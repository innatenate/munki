import random 
from universal import vars
from universal import speechhandle
import re


def choose(phrases):
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase, phrase2, phrase3 = random.choice(phrases), random.choice(phrases), random.choice(phrases)
    phrases = [phrase, phrase2, phrase3]
    phrase = random.choice(phrases)
    return phrase


def checkforSyn(string):
    for x in range(0,2):
        for word in vars.syonyms:
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), string))
            if count >= 3:
                print("replacement")
                string = string.replace(word, choose(vars.syonyms[word]), 2)
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


def makeContext(newContext):

    if vars.context['recentContext']:
        if vars.context['pastContext']:
            vars.context['pastContext'].append(vars.context['recentContext'])
        else:
            vars.context['pastContext'] = [vars.context['recentContext']]
        if len(vars.context['pastContext']) >= vars.context['pastContextMax']:
            vars.context['pastContext'].pop(len(vars.context['pastContext'])-1)

    vars.context['recentContext'] = newContext