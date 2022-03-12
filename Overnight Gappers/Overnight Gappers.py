import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

'''Calculates the change in price in extended hours between the 2 consecutive trading days (row1 and row2).'''
def calcGap(row1, row2):
    close = (row1['Close'])[0] #Gets the closing price from the data at row1
    open = (row2['Open'])[0] #Gets the opening price from the data at row2
    change = (open - close) / close * 100 #Calculates the percent change in price overnight
    return change

'''Takes data from the provided ticker and timeframe and inserts it into a Pandas DataFrame. It then drops the 'Volume' and 'Adj Close' columns.'''
df = yf.download('SPY', datetime(2000, 1, 1), datetime(2020, 1, 1))
df.drop('Volume', axis=1, inplace=True)
df.drop('Adj Close', axis=1, inplace=True)

'''Changes display settings for Pandas dataframes.'''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)

#i and j are indexing variables to use in the while loop.
i = 0 
j = 1

num = 0 #The amount of times the price went down by >1% overnight in the time period.
numIncrease = 0 #Amount of times the price went up the day after it gapped down.
numDecrease = 0 #Amount of times the price went down the day after it gapped down.
avg = 0 #The average change in the price of SPY the day after the price gapped down.
avgIncrease = 0 #The average increase in price the day after it gapped down.
avgDecrease= 0 #The average decrease in price the day after it gapped down.

result = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close'])
increase = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Percent Change'])
decrease = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Percent Change'])

#Iterates through all of the raw data row by row
while (i < len(df) - 1):
    row1 = df.iloc[[i]] #Gets the row at index i of DataFrame df
    row2 = df.iloc[[j]] #Gets the row at index j of DataFrame df

    open = (row2['Open'])[0] #The price at market open the morning after the price gapped down.
    close = (row2['Close'])[0] #The closing price of SPY the day after the price gapped down.
    

    if(calcGap(row1, row2) < -1): #Checks if the price went down by over 1% during extended hours trading.
        result = result.append(row1)
        result = result.append(row2)
        change = (close - open) / open * 100 #The change in price of SPY the day after the price gapped down in %.
        
        if (change < 0):
            '''
            If the price gapped down by >1% and the price continued to decrease the next trading day, appends those 2 rows of data to a 
            separate DataFrame, 'decrease'.
            '''
            decrease = decrease.append(row1)
            decrease = decrease.append(row2)
            avgDecrease += change
            indexDecrease = numDecrease #indexDecrease is a separate variable to index the rows of the 'decrease' DataFrame. 

            '''
            To append the change in price (Percent Change) to the data of each trading day after the price gapped down by >1%, we
            need to be able to index to every other row. When we append row1 and row2 to 'decrease', row2 is the data from the day after 
            the price gapped down and is the data we want to add 'Percent Change' to. As such, for the first set of data appended to decrease, 
            indexDecrease is still 0 so when indexDecrease == 0, we set the value of the cell at row 1 and column 4 (Percent Change) to our 
            change variable because row at index 1 in this case holds the data of 'row2', which is the data we want to add Percent Change to.
            '''
            if (indexDecrease == 0): 
                decrease.iat[1, 4] = f"{round(change, 2)}%"
            else: 
                '''When indexDecrease != 0, we want to access the row at indexDecrease * 2 + 1. For example, for the second set of data
                appended to 'decrease', we want to add Percent Change to the row at index 3 because that holds the data of 'row2' for the second
                set of data appended to 'decrease'. In this second interation, indexDecrease == 1 and as such, indexDecrease * 2 + 1 == 3,
                the index of the row we want to modify.'''
                decrease.iat[indexDecrease * 2 + 1, 4] = f"{round(change, 2)}%"

            numDecrease += 1

        
        elif (change > 0):
            '''
            If the price gapped down by >1% and the price continued to decrease the next trading day, appends those 2 rows of data to a 
            separate DataFrame, 'increase'.
            '''
            increase = increase.append(row1)
            increase = increase.append(row2)
            avgIncrease += change
            indexIncrease = numIncrease

            '''Logic for this if/else block is the same as the if/else inside the 'if (change < 0):' block.'''
            if (indexIncrease == 0):
                increase.iat[1, 4] = f"{round(change, 2)}%"
            else:
                increase.iat[indexIncrease * 2 + 1, 4] = f"{round(change, 2)}%"

            numIncrease += 1

        avg += change
        num += 1
    i += 1
    j += 1

if (avg == 0): #If avg never was changed, there was no data fitting the constraints.
    raise SystemExit("Error: Price never gapped down by more than 1 percent in the selected data.")

#Average change in price, average decrease in price, and average increase in price, respectively. 
avg = round(avg / num, 2)
avgDecrease = round(avgDecrease / numDecrease, 2)
avgIncrease = round(avgIncrease / numIncrease, 2)

k = 1 #Indexing variable used in the while loop.
lHighIndex = 0 #Variable to index the lHigh DataFrame.
hHighIndex = 0 #Variable to index the hHigh DataFrame.
lHigh = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'High vs Open % Change'])
hHigh = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'High vs Open % Change'])

#Copies the data from the 'decrease' DataFrame and drops the 'Percent Change' column.
decrease2 = decrease 
decrease2.drop('Percent Change', axis=1, inplace=True)

#Iterates through each row of the 'decrease2' DataFrame.
while (k < len(decrease2)):
    rowD = decrease2.iloc[[k]] #The row at index k in 'decrease2'.
    highD = (rowD['High'])[0] #The price in the "High" column of 'rowD'.
    openD = (rowD['Open'])[0] #The price in the "Open" column of 'rowD'. 
    changeD = (highD - openD) / openD * 100 #Calculates the change in price in percent between the open and the high of 'rowD'.    

    if (changeD < 0.5):
        '''
        If the change in price between the high and the open is less than 0.5%, appends rowD to a separate DataFrame, 'lHigh'. Then,
        using lHighIndex, inserts 'changeD' into the 'High vs Open % Change' column in the respective row.
        '''
        lHigh = lHigh.append(rowD)
        lHigh.iat[lHighIndex, 4] = f"{round(changeD, 2)}%"
        lHighIndex += 1
    elif(changeD > 0.5):
        '''
        If the change in price between the high and the open is greater than 0.5%, appends rowD to a separate DataFrame, 'hHigh'. Then,
        using hHighIndex, inserts 'changeD' into the 'High vs Open % Change' column in the respective row.
        '''
        hHigh = hHigh.append(rowD)
        hHigh.iat[hHighIndex, 4] = f"{round(changeD, 2)}%"
        hHighIndex += 1
    k += 2

'''A potential trade is at any points of data in 'hHigh' or every other data point in 'increase'. As such, to calculate the percent of 
data points that could result in potentially profitable trades, we add the length of 'hHigh' to the length of 'increase' / 2 and divide that 
by the length of 'result' / 2 and multiply it all by 100 to get it as a percentage.'''
pctPotentialTrades = (len(hHigh) + len(increase) / 2) / (len(result) / 2) * 100

def printData():
    # print("Days the price decreased: ")
    # print(decrease)

    # print("Days the price increased: ")
    # print(increase)

    #print(result)

    # print(f"Average change in price: {avg}%")
    # print(f"Average decrease in price: {avgDecrease}%")
    # print(f"Average increase in price: {avgIncrease}%")

    # print("lHigh Data:")
    # print(lHigh)
    # print("hHigh Data:")
    # print(hHigh)

    #print(f"Percent of potential trades?: {round(pctPotentialTrades, 2)}%")



printData()
