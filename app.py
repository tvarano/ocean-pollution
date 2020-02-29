from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    filt = {}
    print("get called")
    filt = {h: True for h in get_headers()}

    month = request.args.get('month')
    year = request.args.get('year')
    raw = analyze_dataset(filters=filt)
    zones = [k for k in raw if k != None and k.endswith("USA")]
    return render_template('index.html', filters=filt, month=-1, year=-1, data=(json.dumps(raw)), zones=zones)


@app.route('/query', methods=['POST'])
def query(): 
    filt = {h: h in request.form for h in get_headers()}
    month = request.form['month']
    year = request.form['year']
    raw = analyze_month_data(month, year, get_active_headers(filt))
    return json.dumps(raw)

@app.route('/zone', methods=['POST'])
def zone(): 
    filt = json.loads(request.form['filters'])
    #print(request.form)
    #print(request.form["month"])
    #print(request.form["month"] == '-1')
    if (request.form['month'] == '-1'):
        raw = analyze_zone_data(zone=request.form['zone'], filters=filt)
        print("No Month")
    else:
        raw = analyze_zone_data_by_month(zone=request.form['zone'], month=request.form['month'], year=request.form['year'], filters=filt)
    #print(raw)
    raw = {"%f|%f" % k if type(k) == tuple else k: raw[k] for k in raw}
    #print(raw)
    return json.dumps(raw)

def get_active_headers(filt):
    return [k for k in filt if filt[k]]


if __name__ == "__main__":
   app.run(debug=True)
