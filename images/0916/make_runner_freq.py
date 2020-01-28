
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=6)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('runner.csv',encoding='cp932')

df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)
df.drop_duplicates(inplace=True)

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

count = meidai_list['runnerName'].value_counts()
print(count)

plt.hist(count)
plt.savefig('hist.png')