import os
import joblib
from Complexity import calc_complex
from autoArima import get_SARIMA, get_test_data
from sklearn.metrics import mean_squared_error
fields = ['CPLX_FLIGHT_HRS','CPLX_INTER','VERTICAL_INTER_HRS','HORIZ_INTER_HRS','SPEED_INTER_HRS']
ASNPs = ['Skyguide','MUAC','DSNA']
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
def  get_model(ASNP, field, model_type):
    if model_type == 'SARIMA':
        files = os.listdir(directory)
        if ASNP + field + '.pkl' not in files:
            return get_SARIMA(ASNP, field)
        else:
            return joblib.load(f'{directory}/{ASNP + field + '.pkl'}')
    elif model_type == 'EWMA':
        return None
    else:
        return None
    
def get_mses():
    SARIMA_models, EWMA_models = get_models()
    n = len(get_test_data('Skyguide','CPLX_FLIGHT_HRS'))
    mses = {}
    for asnp in ASNPs:
        test_data={}
        predicted_data={}
        for field in ['VERTICAL_INTER_HRS', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'CPLX_INTER', 'CPLX_FLIGHT_HRS']:
            test_data[field] =get_test_data(asnp,field)
            predicted_data[field] = SARIMA_models[asnp + field+'.pkl'].predict(n_periods=n)
        true = calc_complex(test_data)
        prediction = calc_complex(predicted_data)
        mses[asnp] = mean_squared_error(true, prediction)
    return mses    
# #############################################################################

#get the models
SARIMA_models, EWMA_models = get_models()

#get the complexity scores for the test and SARIMA prediction data

print(get_mses())