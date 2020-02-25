from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'POST'): 
        print("POSTED")
    print(request.args.get('filt'))
    month = request.args.get('month')
    year = request.args.get('year')
    raw = analyze_dataset() if (month == 0 and year == 0) else analyze_month_data(month, year)
    return render_template('index.html', filters=filters, month=month, year=year ,data=(json.dumps(raw)))


# def set_activity(activity): 
#     for f in filters: 


filters = {}
for h in get_headers(): 
    filters[h] = True

if __name__ == "__main__":
   app.run(debug=True)
