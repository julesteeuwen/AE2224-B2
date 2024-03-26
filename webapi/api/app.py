from flask import Flask
from flask_cors import CORS, cross_origin
import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
print('this is a test print', parentparentdir)
sys.path.insert(0, parentparentdir) 

from preprocessing import get_data, read_data, ANSPs, split_data, cleanlist

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello():
    return 'hello world'

@app.route('/ansps/<path:name>')
@cross_origin()
def ansp(name):
    ansps = name.split(',')
    TrafficData1 = read_data("../../Datasets/split_2014-2016.csv") #Change to choose CSV file
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
