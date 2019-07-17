'''
Created on 15 lug 2019

@author: smaio

'''

import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class GspeechToTextHelper(object):
    
    def __init__(self):
        pathCredential=os.path.abspath("emotionsproject-e711fd0283dd.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=pathCredential
        #print(os.environ["http_proxy"])
    
    def transcribe(self,filePath,sample_rate,languageCode):
        client = speech.SpeechClient()
        #audio_file=open(filePath,'rb')
        audio_file=filePath
        content=audio_file.read();
        audio=types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=sample_rate,
                    language_code=languageCode)

        response = client.recognize(config, audio)
        results=[]
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            results.append(result.alternatives[0].transcript)
        
        return results
    def transcribeFromBucket(self,gcs_uri,sample_rate,languageCode):
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=sample_rate,
                    language_code=languageCode)

        response = client.recognize(config, audio)
        results=[]
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            results.append(result.alternatives[0].transcript)
        
 
    
    