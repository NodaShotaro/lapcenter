
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('runner.csv',encoding='cp932')
df.drop(columns=[    
    'elapsedRank',
    'elapsedTime',
    'eventName',
    'idealTime',
    'lapRank',
    'lapTime',
    'lossRate',
    'rank',
    'result',
    'runnerId',
    'start',
    'totalLossTime',
    'totalRelative',
    'legNumber'
    ],
    inplace=True)

df['clubName'].fillna('N',inplace=True)

# サンプル数30以下のデータを削除
min_sample = 30

counts = df['runnerName'].value_counts()
delete_list = counts[counts < min_sample].index

for i in delete_list:
        df = df[df['runnerName'] != i]

# 名大生のデータを抽出

#meidai = df[df['clubName'].str.contains('名古屋大学')]['runnerName']
meidai = pd.read_csv('meidai_male.csv',header=None)[0]
delete_list = []

for row in df.itertuples():
    flag = True

    for meidai_name in meidai:
        if(meidai_name == row.runnerName):
            flag = False
    
    if flag:
        delete_list.append(row[0])

meidai_list = df.drop(delete_list)

#agg_all = df.groupby('runnerName').mean()
agg_meidai = meidai_list.groupby('runnerName').mean()

ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
#ax.scatter(agg_all['lossRate'],agg_all['speed'])
#ax.scatter(agg_meidai['legLossTime'],agg_meidai['legSpeed'])
#plt.ylabel('legSpeed')
#plt.xlabel('legLossTime')

#for k in agg_meidai.itertuples():
#        plt.annotate(k[0],(k.lossRate,k.speed),fontproperties=fp)
#plt.savefig("graph.png")

agg_meidai.to_csv('meidai_leg_loss.csv',encoding='cp932')