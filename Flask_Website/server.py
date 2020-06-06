from flask import Flask, render_template, Response, request, jsonify
import json
from glob import glob
from pathlib import Path

app = Flask(__name__)

indexnums=[]
predictions = {}

@app.route('/')
def home():
    indexnums, predictions = read_predsdata()
    print(indexnums)
    return render_template('index.html',data=indexnums)

@app.route('/sentiment')
def sentiment():
    indexno = int(request.args.get('indexno'))
    return render_template('sentiment.html',data=indexno)

def read_predsdata(predfolder='static/preds_data'):
    predfiles = glob(f'{predfolder}/*')
    indexnums=[]
    predictions = {}
    for predfile in predfiles:
        indexno = Path(predfile).stem
        indexnums.append(int(indexno))
        with open(f'{predfile}','r') as fh:
            jsondata = json.load(fh)

        for entry in jsondata['completions'][0]['result']:
            predictions[indexno] = predictions.get(indexno,[]) + [entry['value']] 
            # print(entry['value'])
    return sorted(indexnums), predictions
if __name__=='__main__':
    app.run(debug=True,port=7000)
    indexnums=[]
    predictions = {}