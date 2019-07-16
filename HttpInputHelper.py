'''
Created on 16 lug 2019

@author: maiola_st
'''

import os
import requests
import base64
import io 

class HttpInputHelper(object):
   
    def getFileFromUrl(self,url):
        r=requests.get(url,allow_redirects=True)
        f=io.BytesIO(r.content)
        return f
 
    def getFileFromEncoded(self,encodeString):
        decoded=base64.b64decode(encodeString)
        f=io.BytesIO(decoded)
        return f
 
 
class TrascriviResponse(object):
    def __init__(self,transcriptions,sample_rate,excTime):
        self.transcriptions=transcriptions
        self.sample_rate=sample_rate
        self.execTime=excTime
   
         
class TextSentimentResponse(object):
    def __init__(self,score,magnitude,execTime,content):
        self.score=score
        self.magnitude=magnitude
        self.execTime=execTime
        self.content=content

class ErrorResponse(object):
    def __init__(self,error,message):
        self.error=error
        self.message=message
