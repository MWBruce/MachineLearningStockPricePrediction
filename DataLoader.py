## source myenv/bin/activate
## deactivate

## 0e63f3c385fecfebb04cdcfce62d0ef2


from urllib.request import urlopen
from datetime import datetime, timedelta
import numpy as np
import json
import os
import csv

os.system('clear')

def add_financial_data(revenue_per_share, net_income_per_share, book_value_per_share, 
                       revenue_growth, net_income_growth, book_value_per_share_growth, 
                       three_year_net_income_growth, three_year_revenue_growth, dcf_value, price):

    # Corrected field names
    fieldnames = ['Revenue Per Share', 'Net Income Per Share', 'Book Value Per Share', 
                  'Revenue Growth', 'Net Income Growth', 'Book Value Per Share Growth', 
                  'Three Year Net Income Growth', 'Three Year Revenue Growth', 'DCF Value', 'Price']
    
    directory = "Data"

    if not os.path.exists(directory):
        os.makedirs(directory)

    # New data row
    new_row = [revenue_per_share, net_income_per_share, book_value_per_share, 
               revenue_growth, net_income_growth, book_value_per_share_growth, 
               three_year_net_income_growth, three_year_revenue_growth, dcf_value, price]
    
    # Check if the file does not exist to write headers
    if not os.path.isfile('Data/financial_data.csv'):
        with open('Data/financial_data.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    
    # Write the data
    with open('Data/financial_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

    return



def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def CheckDateCreated(Ticker):
    profile_URL = "https://financialmodelingprep.com/api/v3/profile/" + Ticker + "?apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
    profile = get_jsonparsed_data(profile_URL)
    fin_growth_url = "https://financialmodelingprep.com/api/v3/financial-growth/" + Ticker + "?period=quarter&limit=80&apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
    fin_growth = get_jsonparsed_data(fin_growth_url)
    # Check if the profile data is not empty and 'ipoDate' key exists
    if profile and len(profile[0]['ipoDate']) > 1:   
        ipoDate = datetime.strptime(profile[0]['ipoDate'], '%Y-%m-%d')
        five_years_ago = datetime.now() - timedelta(days=5*365)  
        
        if ipoDate < five_years_ago:
            return True
    return False

def GetInformationForStock(Ticker):
    if not CheckDateCreated(Ticker):
        print("Too Young, Invalid Ticker or Not Enough Avaliable Information")
        return
    dcf_url = "https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/" + Ticker + "?period=quarter&apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
    dcf = get_jsonparsed_data(dcf_url)
    fin_growth_url = "https://financialmodelingprep.com/api/v3/financial-growth/" + Ticker + "?period=quarter&limit=80&apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
    fin_growth = get_jsonparsed_data(fin_growth_url)
    key_metrics_url = "https://financialmodelingprep.com/api/v3/key-metrics/" + Ticker + "?period=quarter&limit=130&apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
    key_metrics = get_jsonparsed_data(key_metrics_url)

    # Parse all dates to datetime objects
    dcf_dates = [datetime.strptime(data['date'], '%Y-%m-%d') for data in dcf]
    fin_growth_dates = [datetime.strptime(data['date'], '%Y-%m-%d') for data in fin_growth]
    key_metrics_dates = [datetime.strptime(data['date'], '%Y-%m-%d') for data in key_metrics]

    # Initialize indices
    dcf_idx = 0
    fin_growth_idx = 0
    key_metrics_idx = 0

    # Until one of the lists runs out
    while dcf_idx < len(dcf_dates) and fin_growth_idx < len(fin_growth_dates) and key_metrics_idx < len(key_metrics_dates):

        # If the dates do not align
        if not (dcf_dates[dcf_idx] == fin_growth_dates[fin_growth_idx] == key_metrics_dates[key_metrics_idx]):

            # Increment the most recent date by one day
            min_date_idx = np.argmax([dcf_dates[dcf_idx], fin_growth_dates[fin_growth_idx], key_metrics_dates[key_metrics_idx]])

            if min_date_idx == 0:
                # Check if it's not the last element in the list
                if dcf_idx < len(dcf_dates) - 1:
                    # print(f"Advancing dcf_idx from {dcf_idx} to {dcf_idx + 1} because {dcf_dates[dcf_idx]} < {fin_growth_dates[fin_growth_idx]} or {key_metrics_dates[key_metrics_idx]}")
                    dcf_idx += 1
                else:
                    # print("Reached the end of dcf data.")
                    break
            elif min_date_idx == 1:
                # Check if it's not the last element in the list
                if fin_growth_idx < len(fin_growth_dates) - 1:
                    # print(f"Advancing fin_growth_idx from {fin_growth_idx} to {fin_growth_idx + 1} because {fin_growth_dates[fin_growth_idx]} < {dcf_dates[dcf_idx]} or {key_metrics_dates[key_metrics_idx]}")
                    fin_growth_idx += 1
                else:
                    # print("Reached the end of fin_growth data.")
                    break
            elif min_date_idx == 2:
                # Check if it's not the last element in the list
                if key_metrics_idx < len(key_metrics_dates) - 1:
                    # print(f"Advancing key_metrics_idx from {key_metrics_idx} to {key_metrics_idx + 1} because {key_metrics_dates[key_metrics_idx]} < {dcf_dates[dcf_idx]} or {fin_growth_dates[fin_growth_idx]}")
                    key_metrics_idx += 1
                else:
                    # print("Reached the end of key_metrics data.")
                    break




        else:
            # Dates align, perform the operations

            # print(dcf[dcf_idx]['date'])
            # print("---------------------------------------------------------")
            # print(key_metrics[key_metrics_idx]['revenuePerShare'])
            # print(key_metrics[key_metrics_idx]['netIncomePerShare'])
            # print(key_metrics[key_metrics_idx]['bookValuePerShare'])
            # print(fin_growth[fin_growth_idx]['revenueGrowth'])
            # print(fin_growth[fin_growth_idx]['netIncomeGrowth'])
            # print(fin_growth[fin_growth_idx]['bookValueperShareGrowth'])
            # print(fin_growth[fin_growth_idx]['threeYNetIncomeGrowthPerShare'])
            # print(fin_growth[fin_growth_idx]['threeYRevenueGrowthPerShare'])
            # print(dcf[dcf_idx]['dcf'])
            # print(dcf[dcf_idx]['price'])
            # print("---------------------------------------------------------")
            # print("\n")




            revenue_per_share = key_metrics[key_metrics_idx]['revenuePerShare']
            net_income_per_share = key_metrics[key_metrics_idx]['netIncomePerShare']
            book_value_per_share = key_metrics[key_metrics_idx]['bookValuePerShare']
            revenue_growth = fin_growth[fin_growth_idx]['revenueGrowth']
            net_income_growth = fin_growth[fin_growth_idx]['netIncomeGrowth']
            book_value_per_share_growth = fin_growth[fin_growth_idx]['bookValueperShareGrowth']
            three_year_net_income_growth = fin_growth[fin_growth_idx]['threeYNetIncomeGrowthPerShare']
            three_year_revenue_growth = fin_growth[fin_growth_idx]['threeYRevenueGrowthPerShare']
            dcf_value = dcf[dcf_idx]['dcf']
            price = dcf[dcf_idx]['price']
            add_financial_data(revenue_per_share, net_income_per_share, book_value_per_share, revenue_growth, net_income_growth,
                       book_value_per_share_growth, three_year_net_income_growth,three_year_revenue_growth, dcf_value, price)

            # Increment all indices
            dcf_idx += 1
            fin_growth_idx += 1
            key_metrics_idx += 1


# url = "https://financialmodelingprep.com/api/v3/sp500_constituent?apikey=0e63f3c385fecfebb04cdcfce62d0ef2"
# sp500Information = get_jsonparsed_data(url)
# for i in range(len(sp500Information)):
#     GetInformationForStock(sp500Information[i]['symbol'])
#     # print(sp500Information[i]['symbol'])


