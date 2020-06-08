from flask import Flask, render_template, Response, request, jsonify
import json
from glob import glob
from pathlib import Path

app = Flask(__name__)


def read_predsdata(predfolder='static/preds_data'):
    predfiles = glob(f'{predfolder}/*')
    indexnums=[]
    predictions = {}
    urls = {}
    for predfile in predfiles:
        indexno = Path(predfile).stem
        indexnums.append(int(indexno))
        with open(f'{predfile}','r') as fh:
            jsondata = json.load(fh)
        
        urls[indexno]=(jsondata['data']['url'])
        for entry in jsondata['completions'][0]['result']:
            predictions[indexno] = predictions.get(indexno,[]) + [entry['value']]
            # print(entry['value'])
    return sorted(indexnums), predictions, urls

indexnums, predictions, urls = read_predsdata()

@app.route('/')
def home():
    return render_template('index.html',data=indexnums)

@app.route('/sentiment')
def sentiment():
    indexno = int(request.args.get('indexno'))
    return render_template('sentiment.html',data=indexno)

@app.route('/getdata',methods=['POST','GET'])
def getdata():
    index = request.args.get('indexno')
    print(predictions[index][-1])
    return jsonify({'preds':predictions[index],'length':predictions[index][-1]['end'],'url':urls[index],'vidurl':urls[index].replace("_bgm","").replace('/mediafiles/','/videofiles/').replace('.mp3','.mp4')})

if __name__=='__main__':
    app.run(debug=True,port=7000)