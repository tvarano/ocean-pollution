from flask import Flask, render_template
import json
from process import *

app = Flask(__name__)

@app.route("/")
def home():
    raw = get_month_data(9, 2018)
    
    return render_template('index.html', data=(json.dumps(raw)))

if __name__ == "__main__":
   app.run(debug=True)
