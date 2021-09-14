
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# class FinancialInstrument():
#     def __init__(self, ticker, price):
#         self.ticker = ticker
#         self.__price = price
#
#     def getPrice(self):
#         return self.__price
#
#     def setPrice(self, new_price):
#         self.__price = new_price
#
#     def __bool__(self):
#         return False
#
# class Portfolio():
#     def __init__(self, instrument, position_size):
#         self.position = instrument
#         self.__size = position_size
#
#     def getValue(self):
#         return self.position.getPrice() * self.__size
#
# AAP = FinancialInstrument('AAP', 20.32)
# myPortfolio = Portfolio(AAP, 100)
# print(myPortfolio.getValue())
# print(myPortfolio._Portfolio__size)
# print(bool(AAP))

class Vector():
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z

    def __getitem__(self, i):
        if i in [0, -3]: return self.x
        elif i in [1, -2]: return self.y
        elif i in [2, -1]: return self.z

    def __iter__(self):
        for i in range(3):
            yield self[i]

v = Vector(1,6,4)

for i in v:
    print(i)
