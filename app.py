from flask import Flask, render_template
from json import JSONEncoder
app = Flask(__name__)

class DataPoint: 
    def __init__(self, lat, long, weight): 
        self.lat = lat
        self.long = long
        self.weight = weight

class DataEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

data = [DataPoint(39.961024, -75.162782, 13.64),
        DataPoint(39.990484, -75.184086, 45.52),
        DataPoint(39.777748, -74.966211, 50.33),
        DataPoint(40.011874, -75.129507, 51.17),
        DataPoint(39.963589, -75.162017, 52.58),
        DataPoint(39.923701, -75.168779, 55.18),
        DataPoint(39.984303, -75.126329, 55.67),
        DataPoint(39.9574, -75.238791, 58.14),
        DataPoint(40.021596, -75.085286, 59.01),
        DataPoint(39.958089, -75.219488, 63.29),
        DataPoint(40.055832, -75.16074, 65.49),
        DataPoint(40.04414, -75.042487, 66.39),
        DataPoint(39.921986, -75.233707, 66.13),
        DataPoint(39.984303, -75.126329, 67.74),
        DataPoint(39.984561, -75.12834, 67.74),
        DataPoint(39.923522, -75.150844, 67.78),
        DataPoint(40.036458, -75.092485, 71.12),
        DataPoint(40.036727, -75.146512, 72.73),
        DataPoint(39.972827, -75.127868, 73.17),
        DataPoint(40.037329, -75.223065, 74.40),
        DataPoint(40.056694, -75.069145, 74.57),
        DataPoint(40.105706, -75.027139, 74.95),
        DataPoint(39.977814, -75.133367, 75.00),
        DataPoint(39.99532, -75.105978, 81.18),
        DataPoint(39.975334, -75.203197, 82.35),
        DataPoint(39.995108, -75.166577, 84.44),
        DataPoint(39.965088, -75.163095, 85.71),
        DataPoint(38.623091, -90.534202, 87.91),
        DataPoint(40.008613, -75.179677, 89.47),
        DataPoint(39.944298, -75.242326, 90.77),
        DataPoint(39.985854, -75.154346, 93.44),
        DataPoint(40.038492, -75.146019, 94.17),
        DataPoint(39.968204, -75.143079, 94.29),
        DataPoint(40.092009, -75.014044, 94.41),
        DataPoint(39.939963, -75.161103, 94.55),
        DataPoint(39.939394, -75.165266, 95.88),
        DataPoint(39.962942, -75.159463, 96.23),
        DataPoint(39.950253, -75.152409, 96.43),
        DataPoint(34.7368, -92.298687, 96.93),
        DataPoint(40.05634, -75.165356, 97.26),
        DataPoint(40.082643, -75.165356, 97.54),
        DataPoint(39.955736, -75.176133, 97.58),
        DataPoint(39.983254, -75.161104, 97.70),
        DataPoint(40.062294, -75.252651, 97.75),
        DataPoint(40.049455, -75.221315, 97.92),
        DataPoint(39.921693, -75.183129, 98.39),
        DataPoint(39.957001, -75.206013, 98.48),
        DataPoint(39.963419, -75.16572, 98.97)]

@app.route("/")
def home():
    print(DataEncoder().encode(data))
    return render_template('index.html', data=(DataEncoder().encode(data)))


if __name__ == "__main__":
   app.run(debug=True)
