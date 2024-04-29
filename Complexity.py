#import stuff
import pandas as pd
import matplotlib.pyplot as plt

#get values
def get_values(file, ansp):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    dataframe = dataframe[dataframe['ENTITY_NAME'] == ansp]
    VERTICAL_INTER_HRS = dataframe['VERTICAL_INTER_HRS']
    HORIZ_INTER_HRS = dataframe['HORIZ_INTER_HRS']
    SPEED_INTER_HRS = dataframe['SPEED_INTER_HRS']
    CPLX_INTER = dataframe['CPLX_INTER']
    CPLX_FLIGHT_HRS = dataframe['CPLX_FLIGHT_HRS']
    return VERTICAL_INTER_HRS, HORIZ_INTER_HRS, SPEED_INTER_HRS, CPLX_INTER, CPLX_FLIGHT_HRS

def calc_values(file, ansp):
    VERTICAL_INTER_HRS, HORIZ_INTER_HRS, SPEED_INTER_HRS, CPLX_INTER, CPLX_FLIGHT_HRS = get_values(file, ansp)
    Adj_Density = CPLX_INTER*60 / CPLX_FLIGHT_HRS
    Struc_Index = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS) / CPLX_INTER
    VERTICAL_INTER = VERTICAL_INTER_HRS*60 / CPLX_FLIGHT_HRS
    HORIZ_INTER = HORIZ_INTER_HRS*60 / CPLX_FLIGHT_HRS
    SPEED_INTER = SPEED_INTER_HRS*60 / CPLX_FLIGHT_HRS
    VERTICAL_SCORE = VERTICAL_INTER_HRS/ CPLX_INTER
    HORIZ_SCORE = HORIZ_INTER_HRS/ CPLX_INTER
    SPEED_SCORE = SPEED_INTER_HRS/ CPLX_INTER
    COMPLEX_SCORE = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS)*60 / CPLX_FLIGHT_HRS
    return Adj_Density,Struc_Index, VERTICAL_INTER, HORIZ_INTER, SPEED_INTER, VERTICAL_SCORE, HORIZ_SCORE, SPEED_SCORE, COMPLEX_SCORE

def calc_complex(data,brief = True):
    '''
    data: dictionary of the form {'VERTICAL_INTER_HRS': [], 'HORIZ_INTER_HRS': [], 'SPEED_INTER_HRS': [], 'CPLX_INTER': [], 'CPLX_FLIGHT_HRS': []}
    '''
    VERTICAL_INTER_HRS, HORIZ_INTER_HRS, SPEED_INTER_HRS, CPLX_INTER, CPLX_FLIGHT_HRS = data['VERTICAL_INTER_HRS'], data['HORIZ_INTER_HRS'], data['SPEED_INTER_HRS'], data['CPLX_INTER'], data['CPLX_FLIGHT_HRS']
    Adj_Density = CPLX_INTER*60 / CPLX_FLIGHT_HRS
    Struc_Index = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS) / CPLX_INTER
    VERTICAL_INTER = VERTICAL_INTER_HRS*60 / CPLX_FLIGHT_HRS
    HORIZ_INTER = HORIZ_INTER_HRS*60 / CPLX_FLIGHT_HRS
    SPEED_INTER = SPEED_INTER_HRS*60 / CPLX_FLIGHT_HRS
    VERTICAL_SCORE = VERTICAL_INTER_HRS/ CPLX_INTER
    HORIZ_SCORE = HORIZ_INTER_HRS/ CPLX_INTER
    SPEED_SCORE = SPEED_INTER_HRS/ CPLX_INTER
    COMPLEX_SCORE = (VERTICAL_INTER_HRS + HORIZ_INTER_HRS + SPEED_INTER_HRS)*60 / CPLX_FLIGHT_HRS
    if not brief:
        return Adj_Density,Struc_Index, VERTICAL_INTER, HORIZ_INTER, SPEED_INTER, VERTICAL_SCORE, HORIZ_SCORE, SPEED_SCORE, COMPLEX_SCORE
    return COMPLEX_SCORE


#Plotting
def plotting(file, ansp, Plot_Copmlex = True, Plot_Adj_Density = False, Plot_Struc_Index = False, Plot_Vertical = False, Plot_Horiz = False, Plot_Speed = False, Plot_Vertical_Score = False, Plot_Horiz_Score = False, Plot_Speed_Score = False):
    Adj_Density, Struc_Index, VERTICAL_INTER, HORIZ_INTER, SPEED_INTER, VERTICAL_SCORE, HORIZ_SCORE, SPEED_SCORE, COMPLEX_SCORE = calc_values(file, ansp)
    if Plot_Copmlex:
        plt.plot(COMPLEX_SCORE, label = "Actual complex score")
        plt.legend()
        plt.title('Complexity Score')
    if Plot_Adj_Density:
        plt.plot(Adj_Density)
        plt.title('Adjusted Density')
    if Plot_Struc_Index:    
        plt.plot(Struc_Index)
        plt.title('Structural Index')
    if Plot_Vertical:
        plt.plot(VERTICAL_INTER)
        plt.title('Vertical Interaction')
    if Plot_Horiz:
        plt.plot(HORIZ_INTER)
        plt.title('Horizontal Interaction')
    if Plot_Speed:
        plt.plot(SPEED_INTER)
        plt.title('Speed Interaction')
    if Plot_Vertical_Score:
        plt.plot(VERTICAL_SCORE)
        plt.title('Vertical Score')
    if Plot_Horiz_Score:
        plt.plot(HORIZ_SCORE)
        plt.title('Horizontal Score')
    if Plot_Speed_Score:
        plt.plot(SPEED_SCORE)
        plt.title('Speed Score')
    plt.show()

#find maximimum value of the parameter and ansp with the maximum value
def find_max_complex(file):
    dataframe = pd.read_csv(file, index_col= 'FLT_DATE',parse_dates=True, date_format='%d-%m-%Y',delimiter=';').dropna()
    ansps = dataframe['ENTITY_NAME'].unique().tolist()
    cplxs = []
    for ansp in ansps:
        Adj_Density, Struc_Index, VERTICAL_INTER, HORIZ_INTER, SPEED_INTER, VERTICAL_SCORE, HORIZ_SCORE, SPEED_SCORE, COMPLEX_SCORE = calc_values(file, ansp)
        cplxs.append(max(COMPLEX_SCORE))
    max_parameter = max(cplxs)
    max_ansp = ansps[cplxs.index(max_parameter)]
    print(f'The maximum value of the parameter is {max_parameter} and the ANSP with the maximum value is {max_ansp}')
    return max_parameter, max_ansp
