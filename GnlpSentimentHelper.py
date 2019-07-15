'''
Created on 15 lug 2019

@author: smaio
'''


from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import time
import os


class GSentimentHelper(object):
    
    def __init__(self):
        pathCredential=os.path.abspath("emotionsproject-e711fd0283dd.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=pathCredential
    
    def analyzeSentiment(self,content,lingua):
        client = language.LanguageServiceClient()
        document = types.Document(
           content=content,
           language=lingua,
           type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        print('Text: {}'.format(content))
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        self.sentiment=SentimentScore(sentiment.score,sentiment.magnitude) 
        
        
        
class SentimentScore:
    def __init__(self,score,magnitude):
        self.score=score
        self.magnitude=magnitude      