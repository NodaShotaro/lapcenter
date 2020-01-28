
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.mstats import gmean

from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('join.csv',encoding='cp932')
df = df[df['runnerName'] == '安部智晴']

#df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)
df.drop_duplicates(inplace=True)

x = df['legSpeed'].sort_values()
n = len(x)

mean = x.sum() / n
g_mean = gmean(x)

alpha_e = mean / gmean * exp()