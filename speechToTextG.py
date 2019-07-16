'''
Created on 15 lug 2019

@author: smaio
'''
from GspeechToTextHelper import GspeechToTextHelper
from GnlpSentimentHelper import GSentimentHelper

from HttpInputHelper import HttpInputHelper




if __name__ == '__main__':
    print("runner")
    #fileUrl="https://emotionsproject.appspot.com/public/audio/cliente1.wav"
    #helper=HttpInputHelper()
    #f=helper.getFileFromUrl(fileUrl)
    #transcribe=GspeechToTextHelper()
    #transcribe.transcribe(f, 44100, "it-IT")
    g=GSentimentHelper();
    g.analyzeSentiment("per me è un problema abito in campagna e attualmente sono senza macchina non posso riportare velo", "it")
    print(g.sentiment.score+' & '+g.sentiment.magnitude)