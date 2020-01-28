
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('runner.csv',encoding='cp932')

df['clubName'].fillna('N',inplace=True)

df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)
df.drop_duplicates(inplace=True)

# サンプル数3以下のデータを削除
min_sample = 3

counts = df['runnerName'].value_counts()
delete_list = counts[counts < min_sample].index

for i in delete_list:
        df = df[df['runnerName'] != i]

agg_all = df.groupby('runnerName').mean()
agg_all.dropna(inplace=True)
#agg_all = agg_all[agg_all['speed'] < 250]

disc_loss = pd.cut(agg_all['lossRate'],10)
disc_speed = pd.cut(agg_all['speed'],10)

lst = []

for s in disc_speed.values.unique():
    for l in disc_loss.values.unique():
        d = {}
        cnt = 0
        for index,t in agg_all.iterrows():
            if t['speed'] in s and t['lossRate'] in l:
                cnt = cnt + 1
        d['speed'] = s.right
        d['lossRate'] = l.right
        d['count'] = cnt
        lst.append(d)

data = pd.DataFrame(lst)
ddata = pd.pivot_table(data=data,
    values='count',
    columns='lossRate',
    index='speed'
)
ddata.sort_index(ascending=False,inplace=True)

ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
sns.heatmap(ddata,square=True,cmap='Blues')

plt.savefig("runner_character.png")
