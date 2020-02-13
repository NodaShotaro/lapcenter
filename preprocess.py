
import pandas as pd
import matplotlib.pyplot as plt
import mylib 
from matplotlib.font_manager import FontProperties

data = pd.read_csv('csv/runner.csv',encoding='utf-8')
data = mylib.completeMissValue(data)

data = mylib.filter_little_race(data,6)
data = mylib.convertLapTime(data,"lapTime")
data = mylib.convertLapTime(data,"legLossTime")
data = mylib.convertLapTime(data,"result")

data = mylib.makeStartPosition(data)

data = mylib.join_with_leginfo(data)
data.to_csv('csv/join.csv',encoding='utf-8',index=False)
