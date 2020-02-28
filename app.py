from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    filt = {}
    print("\n\nget\n\n")
    # print(request)
    filt = {h: True for h in get_headers()}

    month = request.args.get('month')
    year = request.args.get('year')
    raw = analyze_dataset(filters=filt)
    return render_template('index.html', filters=filt, month=-1, year=-1, data=(json.dumps(raw)))


@app.route('/query', methods=['POST'])
def query(): 
    filt = {h: h in request.form for h in get_headers()}
    month = request.form['month']
    year = request.form['year']
    raw = analyze_month_data(month, year, get_active_headers(filt))
    print(raw)
    return json.dumps(raw)

# def set_activity(activity): 
#     for f in filters: 

def get_active_headers(filt):
    return [k for k in filt if filt[k]]


if __name__ == "__main__":
   app.run(debug=True)
