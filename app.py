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
    raw = get_month_data(request.args.get('month'), request.args.get('year'))    
    return render_template('index.html', month=request.args.get('month'), year=request.args.get('year') ,data=(json.dumps(raw)))

if __name__ == "__main__":
   app.run(debug=True)
