'''
Created on 15 lug 2019

@author: smaio
'''
from GBucketHelper import GBucketHelper
import io
from VokaturiHelper import VokaturiHelper
from GspeechToTextHelper import GspeechToTextHelper
import wave
import audioop


if __name__ == '__main__':
    print("runner")
   
    bucketHelper=GBucketHelper()
    #emovo/neu-m3-l2.wav
    (a,b)=bucketHelper.getFileFromBucket("emovo/neu-m3-l2.wav")
    speechHelper=GspeechToTextHelper()
    appolo=speechHelper.convertStereoToMono(b)
    bolla=appolo.getvalue()
    print(bolla)
    fileApp=open("bolla.wav","wb")
    fileApp.write(bolla)
       # audioSeg=AudioSegment(b)
   # audioSeg.set_channels(1)
   # audioSeg.export("gino.wav",format="wav")
    print('fine')
    
    
    #myFiles.delete()
    
    #myFiles.upload_from_filename("c:/appo/twilio.wav")
    
    
    #myFiles.download_to_filename("c:/appo/client1.wav")
    