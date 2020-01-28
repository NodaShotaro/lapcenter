
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

df = pd.read_csv('leg.csv',encoding='cp932')

#等間隔
discrete = pd.cut(df['difficulty'],40).value_counts().sort_index()
discrete = discrete[discrete.values > 10]
disc_ub = []
for i in discrete.index.tolist():
    print(i)
    disc_ub.append(round(i.right))

#等高
discrete_q = pd.qcut(df['difficulty'],5).value_counts().sort_index()

plt.bar(range(0,len(discrete)),discrete.values,tick_label=disc_ub)
plt.xticks(rotation=70,fontproperties=fp)
plt.savefig('legDifficulty.png')
discrete.to_csv('legDifficulty.csv')
plt.clf()

plt.bar(range(0,len(discrete_q)),discrete_q.values,tick_label=discrete_q.index)
plt.xticks(rotation=70)
plt.savefig('legDifficulty_q.png')
discrete.to_csv('legDifficulty_q.csv')