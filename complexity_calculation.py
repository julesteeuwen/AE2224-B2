import pandas as pd


def calculate_scores_daily(data):
    #Calculate individual interaction scores and complexity score for each day

    #Adjusted density
    data["Adjusted_density"] = data["CPLX_INTER"] / data["CPLX_FLIGHT_HRS"] * 60

    #Vertical score
    data["Vertical_score"] = data["VERTICAL_INTER_HRS"] / data["CPLX_INTER"]

    data["Horizontal_score"] = data["HORIZ_INTER_HRS"] / data["CPLX_INTER"]

    data["Speed_score"] = data["SPEED_INTER_HRS"] / data["CPLX_INTER"]

    data["Complexity_score"] = data["Adjusted_density"] * (data["Vertical_score"] + data["Horizontal_score"] + data["Speed_score"])

    return data

def calculate_scores_monthly(data):
    #Group by year and month
    data = data.drop(columns = ['MONTH_MON', 'ENTITY_TYPE', 'ENTITY_NAME'])
    group_month = data.groupby(['YEAR', 'MONTH_NUM']).sum()

    
    #Calculate scores for given month

    return calculate_scores_daily(group_month)

def calculate_scores_yearly(data):
    #Group by year and month
    data = data.drop(columns = ['MONTH_MON', 'ENTITY_TYPE', 'ENTITY_NAME', 'MONTH_NUM'])
    group_year = data.groupby('YEAR').sum()

    
    #Calculate scores for given month

    return calculate_scores_daily(group_year)
