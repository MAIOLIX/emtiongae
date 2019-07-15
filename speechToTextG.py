'''
Created on 15 lug 2019

@author: smaio
'''
from GspeechToTextHelper import GspeechToTextHelper
from GnlpSentimentHelper import GSentimentHelper

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import time
import GnlpSentimentHelper





if __name__ == '__main__':
    print("runner")
    start=time.time()
    speechToText=GspeechToTextHelper()
    textSentiment=GSentimentHelper()
    results=speechToText.transcribe("cliente1.wav", 44100, "it-IT")
    for result in results:
        textSentiment.analyzeSentiment(result,'it')
        print(str(textSentiment.sentiment.score)+' & '+str(textSentiment.sentiment.magnitude))
    
    end=time.time()
    print(end-start)
    #testSpeech()