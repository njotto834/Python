from typing import final
import numpy as np
import pandas as pd
from pandas.io import api
from requests.models import ProtocolError
import requests 
import math

"""Creating an equal-weighted index of the stocks of the S&P 500. sp_500_stocks.csv data is from December 2020.
API data is from the IEX Cloud Sandbox API. Sandbox API data is random."""

#Creates the pandas data frame from sp_500_stocks.csv
stocks = pd.read_csv('sp_500_stocks.csv')
#print(stocks)

"""
How f strings work
    adjective = "cool"
    string = f"FreeCodeCamp is {adjective}"
    print(string)
"""

from secrets import IEX_CLOUD_API_TOKEN
symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()

price = data['latestPrice']
market_cap = data['marketCap']

my_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']
final_data = pd.DataFrame(columns=my_columns)

final_data.append(
    pd.Series(
        [
            symbol,
            price,
            market_cap,
            'N/A'
        ],
        index = my_columns
    ),
    ignore_index = True
)

#Executes an api call for each individual stock ticker
"""Loops through the tickers in our list of stocks and stores the data in a Pandas DataFrame"""
"""
final_data = pd.DataFrame(columns = my_columns)
for stock in stocks['Ticker']:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()

    final_data = final_data.append(
        pd.Series(
            [
                stock,
                data['latestPrice'],
                data['marketCap'],
                'N/A'
            ],
            index = my_columns
        ),
        ignore_index = True
    )
#print(final_data)
"""

#Using Batch API Calls to Improve Performance
def chunks(lst, n):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#Creates 5 full lists with 100 stock tickers each and 1 extra list with the remaining 5 tickers
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
#Parses through each list of stocks in symbol_groups and adds each list of stock tickers to the list symbol_strings
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns = my_columns)

#Parses through each list of stock tickers in symbol_strings and uses those stock tickers to create a batch api call.
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    #For each individual stock ticker in each symbol_string list, appends that stock's data to a Pandas series, which is appended to the final_dataframe.
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'
                ],
                index = my_columns
            ),
            ignore_index=True
        )
#print(final_dataframe)

"""Calculating the Number of Shares to Buy"""
#Takes input from the user to determine size of portfolio.
#try, except ensures that the entered value only contains numbers.
portfolio_size = input('Enter the value of your portfolio in numbers only: ')
try:
    val = float(portfolio_size)
except ValueError:
    print('Please enter an integer')
    portfolio_size = input('Enter the value of your portfolio in numbers only: ')
    val = float(portfolio_size)

position_size = val/len(final_dataframe.index)
totalCost = 0 #Total amount that the shares will end up costing.

#For each row in final_dataframe, sets the value of row i and column 'Number of Shares to Buy' to the maximum of whole shares
#that we can buy of each stock based on our position_size.
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / final_dataframe.loc[i, 'Stock Price'])
    totalCost += final_dataframe.loc[i, 'Number of Shares to Buy'] * final_dataframe.loc[i, 'Stock Price']

#Prints each row in final_dataframe
for i in range(0, len(final_dataframe.index)):
    print(final_dataframe.loc[[i]])

totalCost = round(totalCost, 2)
leftOver = round(val - totalCost, 2)

print()
print("Portfolio Size: $" + str(portfolio_size))
print("Total Cost: $" + str(totalCost))
print("Amount Left: $" + str(leftOver))

