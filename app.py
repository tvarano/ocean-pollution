from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)

# things to fix <3
'''
ok so heres what we have to do...
the form is posting correctly, but it's not passing its args.
i'm just using one big ol form to get all the data (you'll see it)
but its not properly getting the data
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    filt = {}
    if (request.method == 'POST'): 
        for h in get_headers(): 
            filt[h] = h in request.args
            print(h, h in request.args)
     
    else:
        print("get")
        filt = {h: True for h in get_headers()}
    

    month = request.args.get('month')
    year = request.args.get('year')
    raw = analyze_dataset(get_active_headers(filt)) if (month == 0 and year == 0) else analyze_month_data(month, year, get_active_headers(filt))
    return render_template('index.html', filters=filt, month=month, year=year ,data=(json.dumps(raw)))


# def set_activity(activity): 
#     for f in filters: 

def get_active_headers(filt):
    for f, a in enumerate(filt): 
        if a:
            yield f


if __name__ == "__main__":
   app.run(debug=True)
