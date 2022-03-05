import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

def calcGap(row1, row2):
    close = (row1['Close'])[0] #Gets the closing price from the data at row1
    open = (row2['Open'])[0] #Gets the opening price from the data at row2
    change = (open - close) / close * 100 #Calculates the percent change in price overnight
    return change

df = yf.download('SPY', datetime(2018, 1, 1), datetime(2019, 1, 1))
pd.set_option("display.max_rows", None, "display.max_columns", None)

i = 0
j = 1
result = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

while (i < len(df) - 1):
    row1 = df.iloc[[i]] #Gets the row at index i of DataFrame df
    row2 = df.iloc[[j]] #Gets the row at index j of DataFrame df

    '''
    close = row1['Close'] #close becomes a Pandas series containing the closing price data of row1
    open = row2['Open'] #close becomes a Pandas series containing the closing price data of row1
    '''

    if(calcGap(row1, row2) < -1): #Checks if the price went down by over 1% overnight
        result = result.append(row1)
        result = result.append(row2)
    i += 1
    j += 1

print(result)