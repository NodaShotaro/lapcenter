import pandas as pd
import load
import filter_df as fd
import fitting as ft

#df = load.load()
#df = df[df['runnerName'] == '安部智晴']
#df = df[df['legSpeed'] < 500]

#s = ft.df_sample(df,'legSpeed')
#df_hat, loc_hat, scale_hat = ft.chi2_fitting(s,20,'abe.png')


df = load.load()
df = fd.makeLegLabel(df)
df = fd.extractTargetRunner(df,'targetRunnerList.csv')
target_runner = pd.read_csv('targetRunnerList.csv',header=None)[0]

agg = (df.groupby(["runnerName","legJudge"]).count())['classId']
ans = []

for runner in target_runner:

    tmp_sum = agg[runner].sum()
    tmp_list = {}

    for index,row in agg[runner].iteritems():
        tmp_list[index] = row / tmp_sum
    tmp_list["runnerName"] = runner
    ans.append(tmp_list)

pd.DataFrame(ans).round(4).to_csv("rate.csv",encoding='cp932',index=None)

