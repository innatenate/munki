from weather import command as weatherkeys
from questions import command as questionkeys
from universal import vars as vari
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


def process(keys, literal):
    if not query.vars['queryActive']:
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