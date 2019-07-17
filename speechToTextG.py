'''
Created on 15 lug 2019

@author: smaio
'''
from google.cloud import storage
import os
from VokaturiHelper import VokaturiHelper
import io


if __name__ == '__main__':
    print("runner")
    pathCredential=os.path.abspath("emotionsproject-e711fd0283dd.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=pathCredential
    storageClient=storage.Client()
    bucket_name = 'audio-bucket-emotions'
    bucket=storageClient.get_bucket(bucket_name)
    myFiles=bucket.blob('cliente1.wav')
    
    
    file_as_String=myFiles.download_as_string()
    f=io.BytesIO(file_as_String)
    
    
    gcs_uri="gs://audio-bucket-emotions/cliente1.wav"
    #helper=GspeechToTextHelper()
    #helper.transcribeFromBucket(gcs_uri, 44100, "it-IT")
    helper=VokaturiHelper()
    helper.analyzeEmotion(f)
    print(helper.emotions.anger)
    
    
    
    #myFiles.delete()
    
    #myFiles.upload_from_filename("c:/appo/twilio.wav")
    
    
    #myFiles.download_to_filename("c:/appo/client1.wav")
    