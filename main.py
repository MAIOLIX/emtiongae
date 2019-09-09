# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask,request,send_from_directory,json
from sys import platform
from VokaturiHelper import VokaturiHelper
from GspeechToTextHelper import GspeechToTextHelper
from GnlpSentimentHelper import GSentimentHelper
from HttpInputHelper import HttpInputHelper
from HttpInputHelper import ErrorResponse,TrascriviResponse,TextSentimentResponse
from scipy.io import wavfile
import time
from GBucketHelper import GBucketHelper
from flask.helpers import send_file
from flask_cors.extension import CORS



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__) 
v=VokaturiHelper();
transcriber=GspeechToTextHelper()
textSentiment=GSentimentHelper()
fileInputHelper=HttpInputHelper()
bucketHelper=GBucketHelper()
cors=CORS(app)



@app.route('/')
def hello():
    print(platform)
    #print(v.analyzeEmotion("http://localhost:8080/public/audio/cliente1.wav"))
    """Return a friendly HTTP greeting."""
    return app.response_class(response='Never ending story',status=200)

@app.route('/public/<path:path>')
def getStaticResources(path):
    return send_from_directory('public', path)

@app.route('/emotions/audio/analyzeByUrl',methods=['POST'])
def emotions():
    request_json= request.get_json()
    fileUrl=request_json.get('url')
    if fileUrl is not None:
        if fileUrl[0:3]=="gs:":
            print(fileUrl)
            fileUrl=fileUrl[3:]
            (uri,f)=bucketHelper.getFileFromBucket(fileUrl)
            v.analyzeEmotion(f)
            response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
            print(uri)
        else:
            v.analyzeEmotionFromUrl(fileUrl)
            response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
    else :
        response=app.response_class(response='FILE URL missing',status=400)
    return response


@app.route('/emotions/audio/analyzeEmbedded',methods=['POST'])
def emotionEmbedded() :
    request_json=request.get_json()
    encodedFile=request_json.get('wav')
    if encodedFile is not None :
        v.analyzeEmotionFromEncoded(encodedFile)
        response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
    else :
        response=app.response_class(response='encoded ERROR',status=301)

    return response

@app.route('/emotions/transcribe/transcribeByUrl',methods=['POST'])
def trascribeFromUrl():
    start=time.time()
    myRequest=request.get_json()
    myUrl=myRequest.get('url')
    myResponse=None
    myStatus=None
    if myUrl is not None:
        if myUrl[0:3]=='gs:':
            myUrl=myUrl[3:]
            (uri,f)=bucketHelper.getFileFromBucket(myUrl)
        else:
            f=fileInputHelper.getFileFromUrl(myUrl)
        try:
            (sample_rate,samples)=wavfile.read(f)
            print('sample Rate  %.3f Hz' %sample_rate)
            transcriptions=transcriber.transcribe(f, sample_rate, "it-IT")
            end=time.time()
            elapsed=end-start
            myResponse=TrascriviResponse(transcriptions,sample_rate,elapsed)
            myStatus=200
        except:
            myResponse=ErrorResponse('Errore su trascrizione','Errore transcrizione')
            myStatus=400
        finally:
            results=app.response_class(response=json.dumps(myResponse.__dict__),status=myStatus,mimetype='application/json')
    else:
        results=app.response_class(response="Url non trovato",status=400,mimetype='application/json')         
    return results    

@app.route('/emotions/sentiment/analyzeText',methods=['POST'])
def analyzeTextSentiment():
    start=time.time()
    myRequest=request.get_json()
    content=myRequest.get('testo')
    myResponse=None
    myStatus=None
    try :
        if content is not None:
            textSentiment.analyzeSentiment(content, "it")
            end=time.time()
            elapsed=end-start
            myResponse=TextSentimentResponse(textSentiment.sentiment.score,textSentiment.sentiment.magnitude,elapsed,content)
            myStatus=200
        else :
            myStatus=400
            myResponse=ErrorResponse('NO_CONTENT_IN_BODY','Contenuto non trovato nel body')
    except:
        myStatus=400
        myResponse=ErrorResponse('EXCEPTION_RAISE',"Problema nell'analisi del sentiment")
    finally:
        result=app.response_class(response=json.dumps(myResponse.__dict__),status=myStatus,mimetype='application/json')
    return result

@app.route('/emotions/sentiment/analyzeFromFileByUrl',methods=['POST'])
def analyzeSentimentByFile():
    start=time.time()
    myRequest=request.get_json()
    myUrl=myRequest.get('url')
    myResponse=[]
    myStatus=None
    if myUrl is not None:
        if myUrl[0:3]=='gs:':
            myUrl=myUrl[3:]
            (uri,f)=bucketHelper.getFileFromBucket(myUrl)
        else:
            f=fileInputHelper.getFileFromUrl(myUrl) 
        (sample_rate,samples)=wavfile.read(f)
        print('sample Rate  %.3f Hz' %sample_rate)
        transcriptions=transcriber.transcribe(f, sample_rate, "it-IT")
        for transcription in transcriptions : 
            textSentiment.analyzeSentiment(transcription, "it")
            appo=textSentiment.sentiment
            appItem=TextSentimentResponse(appo.score, appo.magnitude, 0, transcription)
            myResponse.append(appItem)
        myStatus=200
    else:
        myStatus=400
        myResponse.append(ErrorResponse('NO_URL_IN_BODY','Url non trovato nel body'))
    result=app.response_class(response=json.dumps([ob.__dict__ for ob in myResponse]),status=myStatus,mimetype='application/json')
    return result

@app.route('/emotions/repository',methods=['GET'])
def getFilesFromBucket():
    nomeFile=request.args.get('file')
    if nomeFile is not None:
        (uri,f)=bucketHelper.getFileFromBucket(nomeFile)
        print(nomeFile)
        return send_file(f, mimetype='audio/wav',attachment_filename=nomeFile)
    else:
        myFileInBucket=bucketHelper.getListBucket()
        result=app.response_class(response=json.dumps([ob.__dict__ for ob in myFileInBucket]),status=200,mimetype='application/json')
        return result



@app.route('/emotions/repository',methods=['POST'])
def uploadFileToBucket():
    responseMessage=None
    responseCode=None
    result=None
    try:
        nomeFile=request.form['nome']
        fileData=request.files['file']
        bucketHelper.uploadFileToBucket(fileData, nomeFile)
        responseMessage="File Caricato"
        responseCode=301
    except:
        responseMessage='Caricamento non avvenuto'
        responseCode=400
    finally:
        result=app.response_class(response=responseMessage,status=responseCode,mimetype='application/json')
    return result


@app.route('/emotions/repository',methods=['DELETE'])
def deleteFileFromBucket():
    nomeFile=request.args.get('file')
    if nomeFile is not None: 
        bucketHelper.deleteFileFromBucket(nomeFile)
        return 'File eliminato'
    else:
        return 'Nessuna operazione eseguita'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
