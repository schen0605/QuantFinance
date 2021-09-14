
import pandas as pd
import numpy as np
import requests

############################

IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'

############################

# PORTFOLIO_VAL = float(input("Enter your portfolio value: "))
PORTFOLIO_VAL = 1_000_000

# try:
#     val = float(PORTFOLIO_VAL)
# except ValueError:
#     PORTFOLIO_VAL = float(input("That's not a number. Please enter your portfolio value: "))

############################

dfColumns = ['Ticker', 'Company', 'Price', 'Market Cap (£ bil)']
df = pd.DataFrame(columns = dfColumns)

temp = np.array(pd.read_excel('FTSE100_List.xlsx')['Ticker'])
tickerList = [temp[:len(temp)//2],temp[len(temp)//2:]]

for i in tickerList:

    temp = '-LN,'.join(i) + '-LN'

    batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?types=quote&symbols={temp}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_url).json()

    for j in range(len(i)):
        new_row = {'Ticker': i[j],
            'Company': data[(i[j]+'-LN')]['quote']['companyName'],
            'Price': data[(i[j]+'-LN')]['quote']['latestPrice'],
            'Market Cap (£ bil)': data[(i[j]+'-LN')]['quote']['marketCap']}
        df = df.append(new_row, ignore_index=True)

totalMarketCap = df['Market Cap (£ bil)'].sum()
weights = df['Market Cap (£ bil)'] / totalMarketCap

df['Weight (%)'] = np.round(weights.values.astype(float) * 100, 2)
df['No. of Shares'] = np.floor(weights * PORTFOLIO_VAL / df['Price'])
df['Price'] = np.round( df['Price'].values.astype(float), 2)
df['Market Cap (£ bil)'] = np.round( df['Market Cap (£ bil)'].values.astype(float)/1E9 , 2)

# print(df)

############################


df.to_excel("output.xlsx")


############################
