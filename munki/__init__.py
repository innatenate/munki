import commands
from commands import keywordtranslate
from commands import speechtranslate

from universal import vars
from universal import uniutils as main


import azure.cognitiveservices.speech as speechsdk
import time
import traceback

sk, sr = "f1231e8177cd4bb98e3f3063d81e7f7b", "eastus"
speechconfig = speechsdk.SpeechConfig(subscription=sk, region=sr)

recognizer = speechsdk.SpeechRecognizer(speech_config=speechconfig)

print("online")
while True:
    time.sleep(1)
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