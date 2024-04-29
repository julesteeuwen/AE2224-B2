def calculate_scores_daily(data):
    """
        Calculate individual interaction scores and complexity score for each day
    """

    #Adjusted density
    data["Adjusted_density"] = data["CPLX_INTER"] / data["CPLX_FLIGHT_HRS"] * 60

    #Vertical score
    data["Vertical_score"] = data["VERTICAL_INTER_HRS"] / data["CPLX_INTER"]

    data["Horizontal_score"] = data["HORIZ_INTER_HRS"] / data["CPLX_INTER"]

    data["Speed_score"] = data["SPEED_INTER_HRS"] / data["CPLX_INTER"]

    data["Structural_index"] = data["Vertical_score"] + data["Horizontal_score"] + data["Speed_score"]

    data["Complexity_score"] = data["Adjusted_density"] * data["Structural_index"]

    

    
    return data


def calculate_scores_weekly(data):
    
    data = data.dropna()
    df = data.reset_index()
    
    #df['FLT_DATE'] = pd.to_datetime(df['FLT_DATE'])

    df['Week_Number'] = df['FLT_DATE'].dt.isocalendar().week

    df = df.groupby(["YEAR", 'Week_Number']).sum(numeric_only = True)
    
    df = calculate_scores_daily(df)

    df = df.reset_index()

   
    
    df['Y-W'] = [str(int(df['YEAR'][i])) + '-' + str(df['Week_Number'][i]) for i in range(len(df))]

    #df = df.drop(['YEAR','Week_Number'])

    df = df.set_index('Y-W')

    

    #print(df)
    return df



def calculate_scores_monthly(data):
    """ Calculate monthly complexity scores for given data """
    #Group by year and month
    
    group_month = data.groupby(['YEAR', 'MONTH_NUM']).sum(numeric_only = True)

    
    #Calculate scores for given month

    data = calculate_scores_daily(group_month)

    data["Y-M"] = [str(int(data.index[i][0]))+'-'+str(int(data.index[i][1])) for i in range(len(data))]

    data = data.set_index("Y-M")

    return data

def calculate_scores_yearly(data):
    """ Calculate yearly complexity scores for given data """
    #Group by year and month
    
    group_year = data.groupby('YEAR').sum(numeric_only = True)

    
    #Calculate scores for given month
    data = calculate_scores_daily(group_year)

    data["Y"] = [int(data.index[i]) for i in range(len(data))]

    data = data.set_index("Y")

    return data

def total_complexity_by_ANSP(data):
    """ Calculate total complexity scores for given data"""
    
    data = data.groupby('ENTITY_NAME').sum(numeric_only = True)

    

    data = calculate_scores_daily(data)


    data_ordered = data.sort_values(by=['Complexity_score'])
    return data_ordered

