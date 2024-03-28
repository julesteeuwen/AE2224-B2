from flask import Flask
from flask_cors import CORS, cross_origin
import sys, os

pardir = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(pardir)

from preprocessing import get_data, read_data, ANSPs, split_data, cleanlist
from complexity_calculation import calculate_scores_daily

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello():
    return 'hello world'

# Retrieve ansps data
@app.route('/ansps/<path:names>')
@cross_origin()
def ansp(names):
    ansps = names.split(',')
    TrafficData1 = read_data(os.path.join(pardir, 'Datasets', 'split_2014-2016.csv')) #Change to choose CSV file
    ANSPs_list = ANSPs(TrafficData1)
    ansps = [ansp for ansp in ansps if ansp in ANSPs_list]
    ANSPs_list = cleanlist(ANSPs_list)
    ANSPsdf = split_data(TrafficData1, ANSPs_list)
    result = '{'
    for ansp in ansps:
        data, name = get_data(ansp, ANSPsdf, ANSPs_list)
        result += ('"' + name + '":' + data.to_json() + ',')

    result = result[:-1]
    result += '}'   

    return result

# Retrieve daily complexity scores
@app.route('/scores/daily/<path:names>')
@cross_origin()
def daily_scores(names):
    ansps = names.split(',')
    TrafficData1 = read_data(os.path.join(pardir, 'Datasets', 'split_2014-2016.csv')) #Change to choose CSV file
    ANSPs_list = ANSPs(TrafficData1)
    ansps = [ansp for ansp in ansps if ansp in ANSPs_list]
    ANSPs_list = cleanlist(ANSPs_list)
    ANSPsdf = split_data(TrafficData1, ANSPs_list)
    result = '{'
    for ansp in ansps:
        data, name = get_data(ansp, ANSPsdf, ANSPs_list)
        data = calculate_scores_daily(data)
        result += ('"' + name + '":' + data.to_json() + ',')

    result = result[:-1]
    result += '}'   
    return result
