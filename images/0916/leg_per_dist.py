
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
dif_disc = pd.cut(df['difficulty'],10)
lng_disc = pd.cut(df['length'],10)


lst = []

for s in dif_disc.values.unique():
    for l in lng_disc.values.unique():
        d = {}
        cnt = 0
        for index,t in df.iterrows():
            if t['difficulty'] in s and t['length'] in l:
                cnt = cnt + 1
        d['difficulty'] = s.right
        d['length'] = l.right
        d['count'] = cnt
        lst.append(d)

data = pd.DataFrame(lst)
ddata = pd.pivot_table(data=data,
    values='count',
    columns='length',
    index='difficulty'
)
ddata.sort_index(ascending=False,inplace=True)

ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
sns.heatmap(ddata,square=True,cmap='Blues')

plt.savefig("leg_per_dist.png")
