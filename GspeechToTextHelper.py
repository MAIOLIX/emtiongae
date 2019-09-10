'''
Created on 15 lug 2019

@author: smaio

'''

import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave
import io
import audioop

class GspeechToTextHelper(object):
    
    def __init__(self):
        pathCredential=os.path.abspath("emoMaiolix-07d9a74a270c.json")
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
        
        return results
    def convertStereoToMono(self,buffer):
        #if self.isStereo(buffer):
        print(buffer.__sizeof__())
        appo=wave.open(buffer, "rb")
        if(appo.getnchannels()==2):
            print("file Stereo")
            buff=io.BytesIO()
            print(buff.__sizeof__())
            mono=wave.open(buff,"wb")
            mono.setparams(appo.getparams())
            mono.setnchannels(1)
            mono.writeframes(audioop.tomono(appo.readframes(float('inf')), appo.getsampwidth(), 1.414, 1.414))
            buff.getbuffer()
            print(buff.__sizeof__())
            mono.close()
            print(buff.__sizeof__())
            return buff
        else:
            print("file Mono")
            return buffer
        
    def isStereo(self,buffer):
        fileInput=wave.open(buffer, "rb")
        channel=fileInput.getnchannels()
        #fileInput.close()
        if channel==2:
            return True
        return False    
                
    