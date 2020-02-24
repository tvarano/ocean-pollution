from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)

class Filter: 
    def __init__(self, title, active): 
        self.title = title
        self.active = active

filters = get_initial_headers()

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'POST'): 
        print("POSTED")
    month = request.args.get('month')
    year = request.args.get('year')
    raw = analyze_dataset() if (month == 0 and year == 0) else analyze_month_data(month, year)
    print(raw)
    return render_template('index.html', month=month, year=year ,data=(json.dumps(raw)))

def get_initial_headers(): 
    for h in get_headers(): 
        filters += Filter(h, True)

def set_activity(activity): 
    for f in filters: 
        


if __name__ == "__main__":
   app.run(debug=True)
