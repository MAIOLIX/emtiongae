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


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
v=VokaturiHelper();
transcriber=GspeechToTextHelper()
textSentiment=GSentimentHelper()
fileInputHelper=HttpInputHelper()

@app.route('/')
def hello():
    print(platform)
    #print(v.analyzeEmotion("http://localhost:8080/public/audio/cliente1.wav"))
   
    """Return a friendly HTTP greeting."""
    return 'Hello World!'







@app.route('/public/<path:path>')
def getStaticResources(path):
    return send_from_directory('public', path)

@app.route('/emotion',methods=['POST'])
def emotions():
    request_json= request.get_json()
    fileUrl=request_json.get('url')
    if fileUrl is not None:
        v.analyzeEmotionFromUrl(fileUrl)
        response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
    else :
        response=app.response_class(response='FILE URL missing',status=400)
    return response


@app.route('/emotions/embedded',methods=['POST'])
def emotionEmbedded() :
    request_json=request.get_json()
    encodedFile=request_json.get('wav')
    if encodedFile is not None :
        v.analyzeEmotionFromEncoded(encodedFile)
        response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
    else :
        response=app.response_class(response='encoded ERROR',status=301)

    return response

@app.route('/emotions/text/transcribe/transcribeByUrl',methods=['POST'])
def trascribeFromUrl():
    start=time.time()
    myRequest=request.get_json()
    myUrl=myRequest.get('url')
    myResponse=None
    myStatus=None
    if myUrl is not None:
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






     

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
