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


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
v=VokaturiHelper();

@app.route('/')
def hello():
    print(platform)
    #print(v.analyzeEmotion("http://localhost:8080/public/audio/cliente1.wav"))
   
    """Return a friendly HTTP greeting."""
    return 'Hello World!'







@app.route('/public/<path:path>')
def getStaticResources(path):
    return send_from_directory('public', path)

@app.route('/emotions',methods=['POST'])
def emotions():
    request_json= request.get_json()
    fileUrl=request_json.get('url')
    if fileUrl is not None:
        v.analyzeEmotionFromUrl(fileUrl)
        response=app.response_class(response=json.dumps(v.emotions.__dict__),status=200,mimetype='application/json')
    else :
        response=app.response_class(response='FILE URL missing',status=301)
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

     

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
