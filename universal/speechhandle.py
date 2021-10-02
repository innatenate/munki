import boto3
from pygame import mixer
import time
import os
from pydub import AudioSegment

polly = boto3.Session(
    aws_access_key_id="AKIAW62R2AZRJ32TRXFJ",
    aws_secret_access_key="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",
    region_name="us-east-1").client('polly')

mixer.init()

spoken = 0

def process(speak):
    global spoken
    spoken += 1
    try:
        response = polly.synthesize_speech(VoiceId="Matthew",
                                            OutputFormat="mp3",
                                            Text=speak,
                                            TextType="ssml",
                                            Engine='neural')
    except Exception as e:
        if e.__traceback__:
            print(repr(e.__traceback__))
        print(repr(e))
        try:
            response = polly.synthesize_speech(VoiceId="Matthew",
                                               OutputFormat="mp3",
                                               Text=speak,
                                               Engine='standard')
        except Exception:
            raise Exception("Unsuccessful text to speech process")
    file = open(f"speech{spoken}.mp3", 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    AudioSegment.from_mp3(f"speech{spoken}.mp3").export(f"speech{spoken}.ogg", format='ogg')
    mixer.music.unload()
    mixer.music.load(f"speech{spoken}.ogg")
    mixer.music.play()
    while mixer.music.get_busy():
        if os.path.exists(f"speech{spoken-1}.ogg"):
            os.remove(f"speech{spoken-1}.ogg")

