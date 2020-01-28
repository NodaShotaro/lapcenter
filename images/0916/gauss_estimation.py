
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('join.csv',encoding='cp932')

#df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)
df.drop_duplicates(inplace=True)


def gauss(mu,sigma):
    return np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) / np.sqrt(2 * np.pi * sigma ** 2)

x = df['legSpeed'].sort_values()
n = len(df)
mu_ML = x.sum() / n
sigma_ML = ((x - mu_ML) ** 2).sum() / n

y_ML = gauss(mu_ML,sigma_ML)

discrete = pd.cut(df['legSpeed'],10).value_counts().sort_index()
disc_ub = []
for i in discrete.index.tolist():
    print(i)
    disc_ub.append(i.right)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

ax.bar(range(0,len(discrete)),discrete.values,tick_label=disc_ub)

ax2 = fig.add_subplot(122)
ax2.plot(x,y_ML)
plt.show()