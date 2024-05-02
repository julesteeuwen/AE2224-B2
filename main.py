from preprocessing import *
# from read_from_file import *
from complexity_calculation import calculate_scores_daily, calculate_scores_monthly, calculate_scores_yearly
# from AUTO_ARIMA import auto_ARIMA




TrafficData1 = read_data("Datasets/split_2017-2019.csv") #Change to choose CSV file

# Initialise the variables
selected_ansps = []
selected_period = ''

# Read the data and split it into ANSPs
ANSPs = ANSPs(TrafficData1)
ANSPs = cleanlist(ANSPs)
ANSPsdf = split_data(TrafficData1, ANSPs)

# data = calculate_scores_daily(data)
# auto_ARIMA(data,"Complexity_score",plotting=True)
if mutlipleseason:
    TrafficData2 = readfilemultipleseason("Datasets/split_2014-2016.csv")
    ANSPsdf = split_data(TrafficData2, ANSPs)
    ANSPName = input("Which ANSP would you want data from?")
    data, ANSPName = get_data(ANSPName, ANSPsdf, ANSPs)
    df = data[["FLT_DATE", "VERTICAL_INTER_HRS"]]
    df.insert(0, 'unique_id', 'HRS')
    df.tail() 
    df = df.rename(columns={"FLT_DATE":'ds',"VERTICAL_INTER_HRS":'y' })
    print(df)
    MultipleSeasonalityDecomp(df, 20)



def clear():
    """ Clear the screen and print the welcome message """
    print("\033[H\033[J", end="")
    print("······························································\n: ____  ____  __  __ _____  _     ____ __  __ _  _____ __  __:\n:/ (__`/ () \|  \/  || ()_)| |__ | ===|\ \/ /| ||_   _|\ \/ /:\n:\____)\____/|_|\/|_||_|   |____||____|/_/\_\|_|  |_|   |__| :\n: _____  ____  ____  _          ____   __  _   ____ _____    :\n:|_   _|/ () \/ () \| |__      / () \ |  \| | (_ (_`| ()_)   :\n:  |_|  \____/\____/|____|    /__/\__\|_|\__|.__)__)|_|      :\n······························································\n")
    print('Welcome to the ANSP Complexity Analysis Tool\n', 
          'Selected ANSPs: ' + ', '.join(selected_ansps) + '\n',
          'Selected Period: ' + selected_period + '\n')
    return

def select_ansps():
    """ Select the ANSPs to analyse """

    # Clear the screen and initialise the variables
    clear()
    selected_ansps.clear()

    # Loop until a valid ANSP is selected
    while True:
        input_ansps = input('Please select the ANSPs you would like to analyse (split by commas): ').split(',')
        all_good = True

        # Check if the input is valid
        for ansp in input_ansps:
            if ansp not in ANSPs:
                print(f"ANSP '{ansp}' not found")
                input_ansps.remove(ansp)
                all_good = False
                continue
            selected_ansps.append(ansp)

        # If all ANSPs are valid, break the loop
        if all_good:
            break
        return

def select_period():
    """ Select the period to analyse """
    global selected_period

    # Clear the screen and initialise the variables
    clear()
    options = ['day', 'month', 'year']
    input_period = ''
    
    # Loop until a valid period is selected
    while True:
        input_period = input('Please select the period you would like to analyse (day, month, year): ')

        # Check if the input is valid
        if input_period not in options:
            print('Invalid period selected')
            continue

        # If valid, set the selected period and break the loop
        selected_period = input_period
        break
    return

def display_graphs():
    """ Display the graphs of the selected ANSPs """
    display_graphs.displaygraphs(ANSPsdf, ANSPs, selected_period, selected_ansps)
    return

# Select the initial ANSPs
select_ansps()

# Select the initial period
select_period()

# Main loop
while True:
    clear()
    print('What do you want to do: ')
    print(' 1. Change ANSPs')
    print(' 2. Change Period')
    print(' 3. Display complexity scores')
    print(' 4. Data Analysis')
    print(' 5. Forecasting')
    print(' 6. Exit')
    input_choice = input('Enter your choice: ')

    # Options dictionary
    options = {
        '1': select_ansps,
        '2': select_period,
        '3': display_graphs,
        '4': exit,
        '5': exit,
        '6': exit
    }

    # Call the function based on the input
    options.get(input_choice, lambda: print('Invalid choice'))()


