import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

def calcGap(row1, row2):
    close = (row1['Close'])[0] #Gets the closing price from the data at row1
    open = (row2['Open'])[0] #Gets the opening price from the data at row2
    change = (open - close) / close * 100 #Calculates the percent change in price overnight
    return change

df = yf.download('SPY', datetime(2000, 1, 1), datetime(2021, 1, 1))
pd.set_option("display.max_rows", None, "display.max_columns", None)

i = 0
j = 1
num = 0 #Variable to track the amount of times the price went down by >1% overnight in the time period.
numIncrease = 0
numDecrease = 0
avg = 0 #The average change in the price of SPY the day after the price gapped down.
avgIncrease = 0
avgDecrease= 0
result = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
increase = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
decrease = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

while (i < len(df) - 1):
    row1 = df.iloc[[i]] #Gets the row at index i of DataFrame df
    row2 = df.iloc[[j]] #Gets the row at index j of DataFrame df

    '''
    close = row1['Close'] #close becomes a Pandas series containing the closing price data of row1
    open = row2['Open'] #close becomes a Pandas series containing the closing price data of row1
    '''
    open = (row2['Open'])[0] #The price at market open the morning after the price gapped down.
    close = (row2['Close'])[0] #The closing price of SPY the day after the price gapped down.
    

    if(calcGap(row1, row2) < -1): #Checks if the price went down by over 1% overnight
        result = result.append(row1)
        result = result.append(row2)
        change = (close - open) / open * 100 #The change in price of SPY the day after the price gapped down in %.

        if (change < 0):
            decrease = result.append(row1)
            decrease = result.append(row2)
            avgDecrease +=change
            numDecrease += 1
        elif (change > 0):
            increase = result.append(row1)
            increase = result.append(row2)
            avgIncrease += change
            numIncrease += 1

        avg += change
        #print(f"{round(change, 2)}%")
        num += 1
    i += 1
    j += 1

if (avg == 0):
    raise SystemExit("Error: Price never gapped down by more than 1 percent in the selected data.")

avg = round(avg / num, 2)
avgDecrease = round(avgDecrease / numDecrease, 2)
avgIncrease = round(avgIncrease / numIncrease, 2)

print("Days the price decreased: ")
print(decrease)

print("Days the price increased: ")
print(increase)

print(f"Average change in price: {avg}%")
print(f"Average decrease in price: {avgDecrease}%")
print(f"Average increase in price: {avgIncrease}%")