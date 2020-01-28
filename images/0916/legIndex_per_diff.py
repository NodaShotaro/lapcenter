
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

df = pd.read_csv('leg.csv',encoding='cp932')
df = df[df['difficulty'] < 500]
dif_disc = pd.cut(df['difficulty'],10)
lindex = df['from'].drop_duplicates().values

lst = []
#等間隔
for s in dif_disc.values.unique():
    for l in lindex:
        d = {}
        cnt = 0
        for index,t in df.iterrows():
            if t['difficulty'] in s and t['from'] == l:
                cnt = cnt + 1
        d['difficulty'] = s.right
        d['from'] = l
        d['count'] = cnt
        lst.append(d)

data = pd.DataFrame(lst)
ddata = pd.pivot_table(data=data,
    values='count',
    columns='from',
    index='difficulty'
)
ddata.sort_index(ascending=False,inplace=True)

ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
sns.heatmap(ddata,square=True,cmap='Blues')

plt.savefig("leg_Index.png")