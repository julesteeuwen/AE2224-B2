import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from sktime.utils.plotting import plot_series
import matplotlib.pyplot as plt
import numpy as np

from EWMA import plot_prediction

from complexity_calculation import calculate_scores_daily

from sktime.forecasting.tbats import TBATS
from sklearn.metrics import mean_absolute_percentage_error as mape
import multiprocessing as mp
import pickle
import csv

########################################################################################

fields = ['CPLX_FLIGHT_HRS', 'CPLX_INTER', 'HORIZ_INTER_HRS', 'SPEED_INTER_HRS', 'VERTICAL_INTER_HRS', 'COMPLEXITY_SCORE']
ANSPs = ['ANS CR', 'ANS Finland', 'ARMATS', 'Albcontrol', 'Austro Control', 'Avinor (Continental)', 'BULATSA', 'Croatia Control', 'DCAC Cyprus', 'DFS', 'DHMI', 'DSNA', 'EANS', 'ENAIRE', 'ENAV', 'HCAA', 'HungaroControl', 'IAA', 'LFV', 'LGS', 'LPS', 'LVNL', 'M-NAV', 'MATS', 'MOLDATSA', 'MUAC', 'NATS (Continental)', 'NAV Portugal (Continental)', 'NAVIAIR', 'Oro Navigacija', 'PANSA', 'ROMATSA', 'SMATSA', 'Sakaeronavigatsia', 'Skyguide', 'Slovenia Control', 'UkSATSE', 'skeyes']

# Importing data
df = pd.read_csv('Datasets/split_2017-2019.csv', index_col='FLT_DATE', parse_dates=True, date_format='%d-%m-%Y')
df.dropna(inplace=True)
df = calculate_scores_daily(df)

plotting = True

smoothing_period = 30

def run_loop(ANSP):
        predicted_values = pd.DataFrame()
        test_values = pd.DataFrame()
        train_values = pd.DataFrame()
        mape_componentwise = None
        mape_total = None
        model = None

        for field in fields:
            # Check if model already exists
            try:
                model = pickle.load(open(f"C:/Users/Jules/Documents/Code/AE2224-B2/SARIMAS/{ANSP}{field}.pkl", 'rb'))
            except Exception as e:
                print(f'C:/Users/Jules/Documents/Code/AE2224-B2/SARIMAS/{ANSP}{field}.pkl not found')

            # Get test data
            df_ansp = df.loc[df['ENTITY_NAME'] == ANSP].copy()
            df_field = df_ansp.loc[:, field].to_frame()
            df_field.index.freq = pd.infer_freq(df_field.index)
            slice = int(0.75 * len(df_field))
            train = df_field[:slice]
            test = df_field[slice:]

            # Update dataframe
            predicted_values[field] = model.predict(len(test))
            test_values[field] = test
            train_values[field] = train

            if field == 'Complexity_score':
                mape_total = mape(test, predicted_values[field])


        predicted_complexity = calculate_scores_daily(predicted_values.copy())

        test_complexity = calculate_scores_daily(test_values)
        mape_componentwise = mape(test_complexity['Complexity_score'], predicted_complexity['Complexity_score'])

        # Plotting
        if plotting:
            fig, axs = plt.subplots(2, 1) 
            fig.set_size_inches(10, 10)
            axs[0].set_title(f'{ANSP} - Componentwise Prediction')
            legend = False
            train_values['Complexity_score'].plot(legend=legend, label='Train', ax=axs[0])
            test_complexity['Complexity_score'].plot(legend=legend, label='Test', ax=axs[0])
            predicted_complexity['Complexity_score'].plot(legend=legend, label='Predicted', ax=axs[0])

            axs[1].set_title(f'{ANSP} - Total Prediction')
            train_values['Complexity_score'].plot(legend=legend, label='Train', ax=axs[1])
            test_complexity['Complexity_score'].plot(legend=legend, label='Test', ax=axs[1])
            predicted_values['Complexity_score'].plot(legend=legend, label='Predicted', ax=axs[1])
            handles, labels = axs[0].get_legend_handles_labels()
            fig.legend(handles, labels, loc='upper right')
            plt.savefig(f'C:/Users/Jules/Documents/Code/AE2224-B2/SARIMAS/plots/{ANSP}_Total.png')


            # Plot componentwise component predictions in one figure
            fig, axs = plt.subplots(len(fields), 1)
            fig.set_size_inches(10, 10)
            for field in fields:
                legend = False
                axs[fields.index(field)].set_title(f'{ANSP} - {field}')
                train_values[field].plot(legend=legend, label='Train', ax=axs[fields.index(field)])
                test_values[field].plot(legend=legend, label='Test', ax=axs[fields.index(field)])
                predicted_values[field].plot(legend=legend, label='Predicted', ax=axs[fields.index(field)])
            handles, labels = axs[0].get_legend_handles_labels()
            fig.legend(handles, labels, loc='upper right')
            plt.savefig(f'C:/Users/Jules/Documents/Code/AE2224-B2/SARIMAS/plots/{ANSP}_Componentwise.png')

        with open(f"C:/Users/Jules/Documents/Code/AE2224-B2/SARIMAS/mape_HWES3.csv", 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([ANSP, mape_total, mape_componentwise])


        print(f"{ANSP} Total mape: {mape_total}")
        print(f"{ANSP} Componentwise mape: {mape_componentwise}")    


if __name__ == '__main__':

    # Multiple cores whooo!
    with mp.Pool(processes=8) as pool:
        pool.map(run_loop, ANSPs)
    
