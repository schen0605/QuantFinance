
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

a = np.random.standard_normal((10, 4))
df = pd.DataFrame(a, columns=['a','b','c','d'],index=["Num" + str(i+1) for i in range(a.shape[0])])
# df['mean']=df.mean(axis=1)
# df['std']=df.std(axis=1)


dates = pd.date_range('2021-1-1',periods = a.shape[0], freq = 'W-MON')
df.index = dates
s = (df['a'] > 0) & (df['c']< 0)
print(type(s))
# df['quarter'] = ['Q1','Q1','Q1','Q1','Q1','Q2','Q2','Q2','Q2','Q4']
# s = df['a']
# print(s, type(s))
# print(df)
# groups = df.groupby('quarter')
# print(groups[['a','d']].mean().round(2))

# df.plot.bar(lw=2.0, xlim=[0,10], figsize=(10, 6), rot=15)
# df.rolling(window=7).mean()['a'].plot(lw=2.0)
# print (dates[7:].values)
# # plt.xlim([dates[7:].values[0],dates[7:].values[-1]])
# s.plot(lw=2.0, figsize=(10, 6), rot=15)
# s.rolling(window=7).mean().plot(lw=2.0)
# plt.show()

# df = pd.DataFrame([[5,1.4],[3,0.2],[1,3.2],[2,1.1]], columns=['num','quan'], index=['a','b','c','d'])
# # print(df.loc['c'])
# # print(df.iloc[1:4].sum())
# # print(df.apply(lambda x: x**2))
#
# # df['extra'] = ['v','f','s','x']
# # print(df['extra'])
#
# df2 = df.append(pd.DataFrame({'quan': 3.4},index=['e']))
# print(df.mean())
