import pandas as pd

df = pd.read_csv("csv/runner_tmp.csv",encoding="utf-8")
df_prev = pd.read_csv("csv/runner.csv",encoding="utf-8")

pd.concat([df,df_prev]).to_csv("csv/runner_concat.csv",encoding="utf-8",index=False)

df = pd.read_csv("csv/leg_tmp.csv",encoding="utf-8")
df_prev = pd.read_csv("csv/leg.csv",encoding="utf-8")

pd.concat([df,df_prev]).to_csv("csv/leg_concat.csv",encoding="utf-8",index=False)