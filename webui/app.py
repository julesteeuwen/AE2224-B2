from flask import Flask

app = Flask(__name__)

# df = pd.read_csv('Datasets/split_2014-2016.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
# df.dropna(inplace=True)

@app.route('/')
def hello():
    return 'hello world'
