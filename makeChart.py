import load
import filter_df
import fitting as ft

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=10)

# dimListを使って集約
# col1，col2を横軸にした散布図を出力
def makeScatter(df,col1,col2,dimList,filename):

        agg_value = target_list.groupby(['runnerName']).mean()

        target_runner = pd.read_csv('targetRunnerList.csv',header=None)[0]

        ans = []
        for runner in target_runner:
                tmp_list = {}
                tmp_list["runnerName"] = runner
                tmp_list["lossRate"] = agg_value["lossRate"][runner]
                tmp_list["speed"] = agg_value["speed"][runner]

                ans.append(tmp_list)

        pd.DataFrame(ans).round(4).to_csv("basic.csv",encoding='cp932',index=None)


        ax = plt.figure(figsize=(12,12)).add_subplot(1,1,1)
        ax.scatter(agg_value['lossRate'],agg_value['speed'])
        plt.ylabel('speed')
        plt.xlabel('lossRate')

        for k in agg_value.itertuples():
                plt.annotate(k[0][0][0:3] +":"+ k[0][1][0:3],(k.lossRate,k.speed),fontproperties=fp)

        plt.savefig(filename)

df = load.load_noleginfo()
df = filter_df.delete_little_runner(df,3,False)    
#df = filter_df.extractByDate(df,2019,3)    
#target_list = filter_df.extractTargetRunner(df,'targetRunnerList.csv')

makeScatter(df,"speed","lossRate",["place"],"scatter_wanami.png")
