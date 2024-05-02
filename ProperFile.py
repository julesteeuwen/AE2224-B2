import os
import joblib
import matplotlib.pyplot as plt 
import pandas as pd
from Complexity import calc_complex
from autoArima import get_SARIMA, get_test_data
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from EWMA import SMA
import multiprocessing as mp
fields = ['COMPLEXITY_SCORE','CPLX_FLIGHT_HRS','CPLX_INTER','VERTICAL_INTER_HRS','HORIZ_INTER_HRS','SPEED_INTER_HRS']
#ASNPs = ['Skyguide','MUAC','DSNA']
ASNPs = ['Albcontrol', 'NAVIAIR', 'LGS', 'Slovenia Control', 'MOLDATSA', 'LVNL', 'DSNA', 'LFV', 'LPS', 'ENAIRE', 'EANS', 'NATS (Continental)', 'Sakaeronavigatsia', 'ARMATS', 'NAV Portugal (Continental)', 'M-NAV', 'skeyes', 'DHMI', 'ENAV', 'DFS', 'DCAC Cyprus', 'HungaroControl', 'MUAC', 'Avinor (Continental)', 'SMATSA', 'ROMATSA', 'Skyguide', 'ANS Finland', 'Croatia Control', 'Oro Navigacija', 'HCAA', 'Austro Control', 'IAA', 'ANS CR', 'UkSATSE', 'MATS', 'PANSA', 'BULATSA']
directory = 'SARIMAS'
def get_EWMA(ASNP, field):
    return None
def read_models(directory):
    models = {}
    files = os.listdir(directory)
    for f in files:
        #joblib.dump(arima, 'arima.pkl')
        models[f]=joblib.load(f'{directory}/{f}')
    return models
def get_models():
    SARIMA_models = read_models('SARIMAS')
    EWMA_models = read_models('EWMAS')
    for field in fields:
        for ASNP in ASNPs:
            key = ASNP + field + '.pkl'
            if key not in SARIMA_models:
                SARIMA_models[key] = get_SARIMA(ASNP, field)
            if key not in EWMA_models:
                EWMA_models[key] = get_EWMA(ASNP, field)
    return SARIMA_models, EWMA_models
def  get_model(ASNP, field, model_type,fake=False):
    if model_type == 'SARIMA':
        files = os.listdir(directory)
        if (ASNP + field +('Sens'if fake else '')+ '.pkl') not in files:
            return get_SARIMA(ASNP, field)
        else:
            return joblib.load(f'{directory}/{ASNP + field +('Sens'if fake else '')+ '.pkl'}')
    elif model_type == 'EWMA':
        return None
    else:
        return None
    
def get_mses(parametered=True):
    #returns the mean squared errors of the models (SARIMA for each comp, SARIMA for the complexity score)
    SARIMA_models, EWMA_models = get_models()
    n = len(get_test_data('Skyguide','CPLX_FLIGHT_HRS'))
    mses = {}
    for asnp in ASNPs:
        test_data={}
        predicted_data={}
        for field in ['VERTICAL_INTER_HRS', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'CPLX_INTER', 'CPLX_FLIGHT_HRS']:
            test_data[field] =get_test_data(asnp,field)
            if parametered:
                predicted_data[field] = SARIMA_models[asnp + field+'.pkl'].predict(n_periods=n)
        true = calc_complex(test_data)
        if parametered:
            prediction = calc_complex(predicted_data)
        prediction2 = SARIMA_models[asnp + 'COMPLEXITY_SCORE'+'.pkl'].predict(n_periods=n)
        mses[asnp] = mean_squared_error(true, prediction) if parametered else mean_squared_error(true, prediction2)
    return mses  
def get_mapes(parametered=True):
    #returns the mean squared errors of the models (SARIMA for each comp, SARIMA for the complexity score)
    SARIMA_models, EWMA_models = get_models()
    n = len(get_test_data('Skyguide','CPLX_FLIGHT_HRS'))
    mapes = {}
    for asnp in ASNPs:
        test_data={}
        predicted_data={}
        for field in ['VERTICAL_INTER_HRS', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'CPLX_INTER', 'CPLX_FLIGHT_HRS']:
            test_data[field] =get_test_data(asnp,field)
            if parametered:
                predicted_data[field] = SARIMA_models[asnp + field+'.pkl'].predict(n_periods=n)
        true = calc_complex(test_data)
        if parametered:
            prediction = calc_complex(predicted_data)
        prediction2 = SARIMA_models[asnp + 'COMPLEXITY_SCORE'+'.pkl'].predict(n_periods=n)
        mapes[asnp] = mean_absolute_percentage_error(true, prediction) if parametered else mean_absolute_percentage_error(true, prediction2)
    return mapes

def predict_complexity(asnp,n,fake=False,parametered=True):
    '''
    asnp: str
    n: int the number of days to predict the complexity for (2yrs+n days)
    prediscts the complexity of the ASNP for the next n days
    '''
    SARIMA_models, EWMA_models = get_models()
    predicted_data={}
    n +=len(get_test_data('Skyguide','CPLX_FLIGHT_HRS'))
    if parametered:
        for field in ['VERTICAL_INTER_HRS', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'CPLX_INTER', 'CPLX_FLIGHT_HRS']:
            predicted_data[field] = SARIMA_models[asnp + field+'.pkl'].predict(n_periods=n)
        #print(predicted_data)
        return calc_complex(predicted_data)
    return SARIMA_models[asnp + 'COMPLEXITY_SCORE'+'.pkl'].predict(n_periods=n)
      

def plot_complexity(asnp,n=365,parametered=True):
    '''
    asnp: str
    plots the complexity of the asnp for the next 365 days
    '''
    datatrain={}
    datatest={}
    for field in ['VERTICAL_INTER_HRS', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'CPLX_INTER', 'CPLX_FLIGHT_HRS']:
        datatest[field] = get_test_data(asnp,field)
        datatrain[field] = get_test_data(asnp,field,return_train=True)
    a = pd.DataFrame(predict_complexity(asnp,n=365,parametered=parametered))
    a.index= pd.date_range(datatest['CPLX_INTER'].index[0], periods=len(a), freq="d")
    #plot train data complexity
    plt.plot(SMA(calc_complex(datatrain),7), color='blue',label='Train samples')
    #plot test data complexity
    plt.plot(SMA(calc_complex(datatest),7), color='red',label='Test samples')
    #plot predicted complexity
    plt.plot(SMA(a,7),label='Forecasts')
    #add the mse to the title
    plt.title(f'SARIMA predictions of complexity for 1 year\nfor {asnp} (mape = {get_mapes(parametered=parametered)[asnp]})')
    plt.legend()
    #make the y axis begin at 0
    plt.ylim(0)
    #save the plot
    plt.savefig(f'SARIMA_GRAPHS/{asnp}_complexity_{'parametered' if parametered else 'not_parametered'}.png')
    plt.cla()
    #plt.show()

def run_loop(ASNP):
    files = os.listdir(directory)
    for field in fields:
            key = ASNP + field + '.pkl'
            if key not in files:
                get_SARIMA(ASNP, field)
    
# #############################################################################

#get the models
with mp.Pool(processes=4) as pool:
        pool.map(run_loop, ASNPs)
SARIMA_models, EWMA_models = get_models()

for asnp in ASNPs:
    plot_complexity(asnp,parametered=False)
    plot_complexity(asnp,parametered=True)

#SMA(df,7)
