'''
Created on 15 lug 2019

@author: smaio
'''
from GBucketHelper import GBucketHelper
import io
from VokaturiHelper import VokaturiHelper
from GspeechToTextHelper import GspeechToTextHelper


if __name__ == '__main__':
    print("runner")
    helper=GBucketHelper()
    (uri,f)=helper.getFileFromBucket('cliente1.wav')
    print(f)
    print(uri)
    v=VokaturiHelper()
    v.analyzeEmotion(f)
    print(v.emotions.anger)
    helper2=GspeechToTextHelper()
    results=helper2.transcribeFromBucket(uri, 44100, "it-IT")
    for result in results:
        print(result)
    
    
    #myFiles.delete()
    
    #myFiles.upload_from_filename("c:/appo/twilio.wav")
    
    
    #myFiles.download_to_filename("c:/appo/client1.wav")
    