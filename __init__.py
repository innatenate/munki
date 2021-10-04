import commands
from commands import keywordtranslate
from commands import speechtranslate

from universal import vars
from universal import uniutils as main

from weather import forecaster

import azure.cognitiveservices.speech as speechsdk
import time
import datetime 
import calendar
import traceback

sk, sr = "f1231e8177cd4bb98e3f3063d81e7f7b", "eastus"
speechconfig = speechsdk.SpeechConfig(subscription=sk, region=sr)

recognizer = speechsdk.SpeechRecognizer(speech_config=speechconfig)
init = True
print("online")
notAnnounced = False
def timers():
    global notAnnounced
    global init
    dt = datetime.datetime.now()
    vars.currentdt = time.time()
    vars.currentH = int(dt.strftime("%H"))
    vars.currentM = int(dt.strftime("%M"))
    vars.currentS = int(dt.strftime("%S"))
    vars.formatTime = dt.strftime("%I:%M %p")
    vars.currentDate = {
        'day': dt.strftime("%A"),
        'numDay': int(dt.strftime("%d")),
        'month': dt.strftime("%B"),
        'numMonth': int(dt.strftime("%m")),
        'year':int(dt.strftime("%Y"))}
    print(f"{vars.currentH}:{vars.currentM}")

    if vars.config['times']['hourannouncement'] and vars.currentM == 0 and notAnnounced:
        notAnnounced = True
        main.speak(main.choose([
            f"The time is now {vars.formatTime}.",
            f"It is now {vars.formatTime}.",
            f"It is currently {vars.formatTime}.",
            f"A new hour has dawned upon us. The time is now {vars.formatTime}.",
            f"Woohoo! Another hour gone. The time is now {vars.formatTime}.",
            f"Another hour has passed. The time is now {vars.formatTime}.",
            f"{vars.formatTime}",
            f"BOO! Did I scare you? The time is now {vars.formatTime}."
        ]))
    elif vars.currentM > 0:
        notAnnounced = False

    if len(vars.alarms) > 0:
        for alarm in vars.alarms:
            if alarm['H'] == vars.currentH and alarm['M'] == vars.currentM:
                alarm['function']()
    if vars.currentM/10 == 1 or vars.currentM/10 == 2 or vars.currentM/10 == 3 or vars.currentM/10 == 4 or vars.currentM/10 == 5 or vars.currentM/10 == 0 or init:
        forecaster.update()
        init = False
while True:
    time.sleep(1)
    timers()
    print("Listening")
    result = recognizer.recognize_once()
    if result:
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            try:
                print(result.text)
                translateResult = speechtranslate.translate(result.text)
            except Exception as e:
                print("\n"*1)
                print(repr(e))
                if e.__traceback__: print(repr(traceback.print_tb(e.__traceback__)))
                if e.__cause__: print(repr(e.__cause__))
                if e.__context__: print(repr(e.__context__))

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

