from flask import Flask, render_template, request
import json
from process import *

app = Flask(__name__)

class Date: 
    def __init__(self, month, year): 
        self.month = month
        self.year = year

@app.route('/', methods=['GET', 'POST'])
def home():
    month = request.args.get('month')
    year = request.args.get('year')
    raw = get_month_data(None if month == 0 else month, None if year == 0 else year)
    print(raw)
    return render_template('index.html', month=month, year=year ,data=(json.dumps(raw)))

if __name__ == "__main__":
   app.run(debug=True)
