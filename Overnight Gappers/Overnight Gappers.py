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
df.drop('Volume', axis=1, inplace=True)
df.drop('Adj Close', axis=1, inplace=True)

#pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)

i = 0
j = 1
num = 0 #The amount of times the price went down by >1% overnight in the time period.
numIncrease = 0 #Amount of times the price went up the day after it gapped down.
numDecrease = 0 #Amount of times the price went down the day after it gapped down.
avg = 0 #The average change in the price of SPY the day after the price gapped down.
avgIncrease = 0 #The average increase in price the day after it gapped down.
avgDecrease= 0#The average decrease in price the day after it gapped down.

result = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Percent Change'])
increase = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Percent Change'])
decrease = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Percent Change'])

#Iterates through all of the data row by row
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
        result.iat[num, 4] = round(change, 2)
        
        if (change < 0):
            decrease = decrease.append(row1)
            decrease = decrease.append(row2)
            avgDecrease += change
            indexDecrease = numDecrease

            if (indexDecrease == 0):
                decrease.iat[1, 4] = f"{round(change, 2)}%"
            else:
                decrease.iat[indexDecrease * 2 + 1, 4] = f"{round(change, 2)}%"

            numDecrease += 1

        elif (change > 0):
            increase = increase.append(row1)
            increase = increase.append(row2)
            avgIncrease += change
            indexIncrease = numIncrease

            if (indexIncrease == 0):
                increase.iat[1, 4] = f"{round(change, 2)}%"
            else:
                increase.iat[indexIncrease * 2 + 1, 4] = f"{round(change, 2)}%"

            numIncrease += 1

        avg += change
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

# print(result)

print(f"Average change in price: {avg}%")
print(f"Average decrease in price: {avgDecrease}%")
print(f"Average increase in price: {avgIncrease}%")