
import pandas as pd
import numpy as np
import requests
from scipy import stats

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

TICKER_LIST = chunks(np.array(pd.read_excel('SP500_List.xlsx')['Ticker']), 100) # batched api call

############################
# Simple weighting using just PE Ratio
############################

# dfColumns = ['Ticker', 'Company', 'Price', 'PE Ratio']
# df = pd.DataFrame(columns = dfColumns)
#
#
# for i in TICKER_LIST:
#
#     temp = ','.join(i)
#
#     batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=advanced-stats,quote&symbols={temp}&token={IEX_CLOUD_API_TOKEN}'
#
#     data = requests.get(batch_api_url).json()
#
#     for j in range(len(i)):
#         new_row = {'Ticker': i[j],
#             'Company': data[(i[j])]['advanced-stats']['companyName'],
#             'Price': data[(i[j])]['quote']['latestPrice'],
#             'PE Ratio': data[(i[j])]['advanced-stats']['peRatio'],
#             }
#         df = df.append(new_row, ignore_index=True)
#
# df.sort_values('PE Ratio', inplace = True)
# df = df[df['PE Ratio'] > 0] # remove negative PE ratios
# df = df[:50]
# df.reset_index(inplace = True)
# df.drop('index', axis=1, inplace = True)
#
# totalPERatio = df['PE Ratio'].sum()
# weights = df['PE Ratio'] / totalPERatio
#
# df['Weight (%)'] = np.round(weights.values.astype(float) * 100, 2)
# df['No. of Shares'] = np.floor(weights * PORTFOLIO_VAL / df['Price'])
# df['Price'] = np.round( df['Price'].values, 2)
# df['PE Ratio'] = np.round( df['PE Ratio'].values , 2)

# print(df)

############################

# df.to_excel("output.xlsx")

############################
# Weighting using multiple ratios with adjustable weightings for each ratio:
PE_RATIO_WEIGHTING = 0.3
PB_RATIO_WEIGHTING = 0.1
PS_RATIO_WEIGHTING = 0.1
EV_EBITDA_WEIGHTING = 0.3
EV_GP_WEIGHTING = 0.2
############################

df2Columns = ['Ticker', 'Company', 'Price', 'PE Ratio', 'PB Ratio', 'PS Ratio', 'EV/EBITDA', 'EV/GP']
df2 = pd.DataFrame(columns = df2Columns)

for i in TICKER_LIST:

    temp = ','.join(i)

    batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=advanced-stats,quote&symbols={temp}&token={IEX_CLOUD_API_TOKEN}'

    data = requests.get(batch_api_url).json()

    for j in range(len(i)):

        enterpriseValue = data[(i[j])]['advanced-stats']['enterpriseValue']

        try:
            EV_to_EBITDA = enterpriseValue / data[(i[j])]['advanced-stats']['EBITDA']
        except TypeError:
            EV_to_EBITDA = np.NaN

        try:
            EV_to_GP = enterpriseValue / data[(i[j])]['advanced-stats']['grossProfit']
        except TypeError:
            EV_to_GP = np.NaN

        new_row = {'Ticker': i[j],
            'Company': data[(i[j])]['advanced-stats']['companyName'],
            'Price': data[(i[j])]['quote']['latestPrice'],
            'PE Ratio': data[(i[j])]['advanced-stats']['peRatio'],
            'PB Ratio': data[(i[j])]['advanced-stats']['priceToBook'],
            'PS Ratio': data[(i[j])]['advanced-stats']['priceToSales'],
            'EV/EBITDA': EV_to_EBITDA,
            'EV/GP': EV_to_GP
            }
        df2 = df2.append(new_row, ignore_index=True)

df2.dropna(inplace = True) # drop any stocks that has incomplete data
df2.reset_index(inplace = True)
df2.drop('index', axis=1, inplace = True)

overall_weight = np.zeros(len(df2.index))

for row in df2.index:

    PE_percentile = stats.percentileofscore(df2['PE Ratio'], df2.loc[row, 'PE Ratio']) / 100
    PB_percentile = stats.percentileofscore(df2['PB Ratio'], df2.loc[row, 'PB Ratio']) / 100
    PS_percentile = stats.percentileofscore(df2['PS Ratio'], df2.loc[row, 'PS Ratio']) / 100
    EV_EBITDA_percentile = stats.percentileofscore(df2['EV/EBITDA'], df2.loc[row, 'EV/EBITDA']) / 100
    EV_GP_percentile = stats.percentileofscore(df2['EV/GP'], df2.loc[row, 'EV/GP']) / 100

    overall_weight[row] = PE_RATIO_WEIGHTING * PE_percentile + PB_RATIO_WEIGHTING * PB_percentile + PS_RATIO_WEIGHTING * PS_percentile + EV_EBITDA_WEIGHTING * EV_EBITDA_percentile + EV_GP_WEIGHTING * EV_GP_percentile

df2['Weighting (%)'] = overall_weight

df2.sort_values('Weighting (%)', ascending = False, inplace = True)
df2 = df2[:50]
df2.reset_index(inplace = True)
df2.drop('index', axis=1, inplace = True)

totalWeight = df2['Weighting (%)'].sum()
df2['Weighting (%)'] = np.round((df2['Weighting (%)']/totalWeight) * 100, 2)
df2['No. of Shares'] = np.floor(df2['Weighting (%)'] * PORTFOLIO_VAL / df2['Price'])
df2['Price'] = np.round(df2['Price'].values.astype(float), 2)
df2['PE Ratio'] = np.round(df2['PE Ratio'].values.astype(float), 2)
df2['PB Ratio'] = np.round(df2['PB Ratio'].values.astype(float), 2)
df2['PS Ratio'] = np.round(df2['PS Ratio'].values.astype(float), 2)
df2['EV/EBITDA'] = np.round(df2['EV/EBITDA'].values.astype(float), 2)
df2['EV/GP'] = np.round(df2['EV/GP'].values.astype(float), 2)

# print(df2)

df2.to_excel("CompositeValueStrat.xlsx")


######################
