
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

def chunks(lst, n):
    # Yield successive n-sized chunks from lst.
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

############################
# Simple weighting using just PE Ratio
############################

dfColumns = ['Ticker', 'Company', 'Price', 'PE Ratio']
df = pd.DataFrame(columns = dfColumns)

tickerList = chunks(np.array(pd.read_excel('SP500_List.xlsx')['Ticker']), 100) # batched api call

for i in tickerList:

    temp = ','.join(i)

    batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=advanced-stats,quote&symbols={temp}&token={IEX_CLOUD_API_TOKEN}'

    data = requests.get(batch_api_url).json()

    for j in range(len(i)):
        new_row = {'Ticker': i[j],
            'Company': data[(i[j])]['advanced-stats']['companyName'],
            'Price': data[(i[j])]['quote']['latestPrice'],
            'PE Ratio': data[(i[j])]['advanced-stats']['peRatio'],
            }
        df = df.append(new_row, ignore_index=True)

df.sort_values('PE Ratio', inplace = True)
df = df[df['PE Ratio'] > 0] # remove negative PE ratios
df = df[:50]
df.reset_index(inplace = True)
df.drop('index', axis=1, inplace = True)

totalPERatio = df['PE Ratio'].sum()
weights = df['PE Ratio'] / totalPERatio

df['Weight (%)'] = np.round(weights.values.astype(float) * 100, 2)
df['No. of Shares'] = np.floor(weights * PORTFOLIO_VAL / df['Price'])
df['Price'] = np.round( df['Price'].values.astype(float), 2)
df['PE Ratio'] = np.round( df['PE Ratio'].values.astype(float)/1E9 , 2)

print(df)

############################


# df.to_excel("output.xlsx")


############################
