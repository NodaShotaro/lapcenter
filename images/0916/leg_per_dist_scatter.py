
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('leg.csv',encoding='cp932')
df = df[['difficulty','length']]
df = df[df['difficulty'] < 400]
df = df[df['length'] < 30]

ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
ax.scatter(df['length'],df['difficulty'])
plt.ylabel('difficulty')
plt.xlabel('length')

#for k in agg_meidai.itertuples():
#        plt.annotate(k[0],(k.lossRate,k.speed),fontproperties=fp)
#plt.savefig("graph.png")

plt.savefig("leg_per_dist_scatter.png")
