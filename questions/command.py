from universal import uniutils as uni
from universal import vars

import datetime
from randfacts import get_fact
from newsapi import NewsApiClient
import traceback


api = NewsApiClient(api_key="efe6facd2ffc41d7b4744391e34ff068")

keys = []
qb = {}

### Weather: Questionbank
###     'temp' :  Question
###             'keys'  :   ['what is the current temperature', 'what does it feel like outside', 'what is the temperature outside']
###             'function' : def func()
###             'require' : optional, require keys


qb['timecheck'] = {}
qb['timecheck']['keys'] = ["what is the time", "what is the current time", "what time is it"]
qb['timecheck']['require'] = ["time"]
def timeCheck(keywords, data=False, passedValue=False):
    now = datetime.datetime.now()
    phrase = uni.choose([f"The current time is {now.strftime('%I:%M %p')}.",
                             f"It's currently {now.strftime('%I:%M %p')}.",
                             f"The time now is {now.strftime('%I:%M %p')}",
                             now.strftime('%I:%M %p'),
                             f"It is currently {now.strftime('%I:%M %p')}"])
    uni.speak(phrase)
    return True
qb['timecheck']['function'] = timeCheck


qb['repeat'] = {}
qb['repeat']['keys'] = ['repeat', 'say again', 'repeat that', 'say that again']
def repeat(keywords, data=False, passedValue=False):
    phrase = uni.choose(["I said, ", "No problem, I said", "Alright, "])
    phrase += "             " + vars.phrases['lastPhrase']

    uni.speak(phrase)
    return True
qb['repeat']['function'] = repeat


qb['newscheck'] = {}
qb['newscheck']['keys'] = ["what is today's news", "what is the news for today", "what is happening",
                           "what is the daily news", "what's the news"]
def newsCheck(keywords, data=False, passedValue=False):
    results = api.get_top_headlines(country="us", page_size=5)
    results = [
        {
            'author': results['articles'][0]['author'],
            'desc': results['articles'][0]['description']
        },
        {
            'author': results['articles'][1]['author'],
            'desc': results['articles'][1]['description']
        },
        {
            'author': results['articles'][2]['author'],
            'desc': results['articles'][2]['description']
        },
        {
            'author': results['articles'][3]['author'],
            'desc': results['articles'][3]['description']
        },
        {
            'author': results['articles'][4]['author'],
            'desc': results['articles'][4]['description']
        },
    ]
    uni.speak("Today's top news. \n" +
                    f"{results[0]['author']} reports {results[0]['desc']} \n \n" +
                    f"I also found {results[1]['author']} reporting on {results[1]['desc']} \n" +
                    f"On {results[2]['author']} I found an article on {results[2]['desc']} \n \n \n" +
                    f"{results[3]['author']} reports {results[3]['desc']} \n \n" +
                    f"And lastly, {results[4]['author']} wrote an article recently on {results[4]['desc']}")
    return True
qb['newscheck']['function'] = newsCheck

qb['datecheck'] = {}
qb['datecheck']['keys'] = ["what is today numerical", "what is today's date", "what is the date today"]
def dateCheck(keywords, data=False, passedValue=False):
    now = datetime.datetime.now()
    uni.speak(f"Today is {now.strftime('%A    , %B %d     %Y')}")

    return True
qb['datecheck']['function'] = dateCheck


def mathCheck(keywords):
    for word in keywords:
        if len(word) == 1:
            return True
    return False


def calculate(keywords):
    for word in keywords:
        if len(word) > 1:
            keywords.remove(word)

    try:
        keywords = ''.join(keywords)
        answer = eval(keywords)
        return answer, keywords
    except Exception as e:
        print("[ERRO]: " + repr(e))
        traceback.print_tb(e.__traceback__)
        return False, False


def process(keywords, info, passedValue=False, client=False, override=False):
    """Process question commands, needs keywords(list) and can take a passedValue(any)"""

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
                success = qb[choice[0]]['function'](keywords, info, passedValue)
                debounce = True

        if success:
            return True
        else:
            return False
    else:
        if ("what" in keywords or "what's" in keywords) and mathCheck(keywords):
            answer, problem = calculate(keywords)
            if not answer:
                phrase = uni.choose(["I couldn't seem to find an answer to that math problem.",
                                         "I couldn't calculate the correct answer.",
                                         "Something didn't process correctly with that equation."])
            else:
                phrase = uni.choose([f"The answer to {problem} is {answer}.",
                                         f"When I processed {problem}, I concluded {answer}.",
                                         f"I calculated {problem} with the end result of {answer}."])

            uni.speak(phrase)
            return True
        else:
            return Exception("No result")
            # answer = searchparser.search(originaltext)
            # if answer:
            # if 'snippet' in answer:
            # uni.speak(f"I searched that for you. {answer['answer']}. I also have more information, "
            # f"{answer['snippet']}")
            # elif 'answer' in answer:
            # uni.speak(f"I searched that for you.  {answer['answer']}.")
            # elif 'error' in answer:
            # uni.speak(answer['error'])
            # return True

for function in qb:
    for key in qb[function]['keys']:
        keys.append(key)
