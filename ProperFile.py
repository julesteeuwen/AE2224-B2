import os
import joblib
from autoArima import get_SARIMA
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
    fields = ['CPLX_FLIGHT_HRS','CPLX_INTER','VERTICAL_INTER_HRS','HORIZ_INTER_HRS','SPEED_INTER_HRS']
    ASNPs = ['Skyguide','MUAC','DSNA']
    for field in fields:
        for ASNP in ASNPs:
            key = ASNP + field + '.pkl'
            if key not in SARIMA_models:
                SARIMA_models[key] = get_SARIMA(ASNP, field)
            if key not in EWMA_models:
                EWMA_models[key] = get_EWMA(ASNP, field)
    return SARIMA_models, EWMA_models