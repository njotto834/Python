import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

def calcGap(row1, row2):
    close = (row1['Close'])[0]
    open = (row2['Open'])[0]
    change = (open - close) / close * 100 #Calculates the percent change in price overnight
    return change

df = yf.download('SPY', datetime(2018, 1, 1), datetime(2019, 1, 1))
df2 = yf.download('SPY', datetime(2018, 1, 3), datetime(2019, 1, 3))
pd.set_option("display.max_rows", None, "display.max_columns", None)

# print(df)
# print(df2)
# print(len(df))
# print(len(df2))
# print(df.columns)
# print(df2.columns)
# print(df.iloc[[0]])


# testDF = df.iloc[[0]]
# for row2 in testDF.itertuples():
#     print(row2)

# for row in df.itertuples(): 
#     print(row)
#     # close = getattr(row, 'Close')
#     # print(close)

if (len(df) != len(df2)):
    raise SystemExit('Error: Dataframes are not of equal length.')

i = 0
j = 1
result = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

while (i < len(df) - 1):
    row1 = df.iloc[[i]]
    row2 = df.iloc[[j]]
    close = row1['Close']
    open = row2['Open']
    
    

    # print(row1['Close'])
    # print(row2['Open'])
    if(calcGap(row1, row2) < -1):
        # result = pd.concat([result, row1, row2], axis=0)
        result = result.append(row1)
        result = result.append(row2)
    i += 1
    j += 1

print(result)