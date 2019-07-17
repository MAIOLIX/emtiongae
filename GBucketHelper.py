'''
Created on 17 lug 2019

@author: smaio
'''
from google.cloud import storage,exceptions
import os
import io


class GBucketHelper(object):
    def __init__(self):
        pathCredential=os.path.abspath("emotionsproject-e711fd0283dd.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=pathCredential
        self.bucketRoot="audio-bucket-emotions"
        self.storageClient=storage.Client()
        self.bucket=self.storageClient.get_bucket(self.bucketRoot)
        self.gsRootUri="gs://audio-bucket-emotions/"
    
    def getListBucket(self):
        myFiles=self.bucket.list_blobs()
        myResult=[]
        for myFile in myFiles :
            strApp=self.gsRootUri+myFile.name
            fileO=FileOBJ(myFile.name,strApp)
            myResult.append(fileO)
        return myResult

    def getFileFromBucket(self,filename):
        strApp=None
        f=None
        try:
            myFile=self.bucket.blob(filename)
            file_as_String=myFile.download_as_string()
            f=io.BytesIO(file_as_String)
            strApp=self.gsRootUri+filename
        except exceptions.NotFound:
            print('File not found')
        finally :
            return (strApp,f)

    def uploadFileToBucket(self,myBytes,myFileName):
        f=self.bucket.blob(myFileName)
        f.upload_from_file(myBytes)
    
    def deleteFileFromBucket(self,myFileName):
        try:
            f=self.bucket.blob(myFileName)
            f.delete()
            return True
        except exceptions.NotFound :
            print('File not found')
            return False


class FileOBJ(object):
    def __init__(self,nome,uri):
        self.nome=nome
        self.uri=uri