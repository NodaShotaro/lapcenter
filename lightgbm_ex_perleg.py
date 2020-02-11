import load 

import pandas as pd
import lightgbm as lgb

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

df = load.load()
df.dropna(subset=["runnerName"],inplace=True)
df.fillna({"prefacture" : "Empty", "clubName": "Empty"},inplace=True)

runner = LabelEncoder()
runner = runner.fit(df["runnerName"])
df["runnerName_L"] = runner.transform(df["runnerName"])

club = LabelEncoder()
club = club.fit(df["clubName"])
df["clubName_L"] = club.transform(df["clubName"])

place = LabelEncoder()
place = place.fit(df["prefacture"])
df["prefacture_L"] = place.transform(df["prefacture"])

df["race_L"] = df["eventName"] + df["classId"].astype(str)
event = LabelEncoder()
event = event.fit(df["race_L"])
df["race_L"] = event.transform(df["race_L"])

df["month"] = df["date"].dt.month

valid = df[(df["eventName"] == "2019年度日本学生オリエンテーリング選手権大会　ロング・ディスタンス競技部門") | (df["eventName"] == "2018年度日本学生オリエンテーリング選手権大会　ミドル・ディスタンス競技部門") | (df["eventName"] == "第16回東海学生オリエンテーリング選手権大会")]
df = df[~((df["eventName"] == "2019年度日本学生オリエンテーリング選手権大会　ロング・ディスタンス競技部門") | (df["eventName"] == "2018年度日本学生オリエンテーリング選手権大会　ミドル・ディスタンス競技部門") | (df["eventName"] == "第16回東海学生オリエンテーリング選手権大会"))]

query = df.groupby("race_L").count()
query_v = valid.groupby("race_L").count()

lgtrain = lgb.Dataset(df[["runnerName_L","prefacture_L"]].values, df["lapRank"].values, categorical_feature=[0,1],group=query["runnerName"])
lgvalid = lgb.Dataset(valid[["runnerName_L","prefacture_L"]].values, valid["lapRank"].values, categorical_feature=[0,1],group=query_v["runnerName"])

label_gain = []

for i in range(0,5000):
	label_gain.append(2^i -1)

max_position = 100
lgbm_params =  {
	'task': 'train',
	'boosting_type': 'gbdt',
	'objective': 'lambdarank',
	'metric': 'ndcg',   # for lambdarank
	'ndcg_eval_at': list(range(1,max_position)),  # for lambdarank
	'max_position': max_position,  # for lambdarank
	'learning_rate': 0.1,
	'min_data': 1,
	'min_data_in_bin': 1,
	'label_gain' : label_gain
}


lgb_clf = lgb.train(
	lgbm_params,
	lgtrain,
	categorical_feature=[0,1],
	num_boost_round=100,
	valid_sets=[lgtrain, lgvalid],
	valid_names=['train','valid'],
	verbose_eval=1
)

# 予測用コード
# 男子の予想
target = pd.read_csv("targetRunnerList_m.csv")
target["prefacture"] = "栃木"
target["runnerName_L"] = runner.transform(target["runnerName"])
target["prefacture_L"] = place.transform(target["prefacture"])

y_predict = lgb_clf.predict(target[["runnerName_L","prefacture_L"]].values)
target["score"] = y_predict
target["rank"] = target.rank(method="min")["score"]
target[["rank","runnerName","score"]].sort_values("score").to_csv("predict_me.csv",encoding="cp932")

#女子の予想
target = pd.read_csv("targetRunnerList.csv")
target["prefacture"] = "栃木"
target["runnerName_L"] = runner.transform(target["runnerName"])
target["prefacture_L"] = place.transform(target["prefacture"])

y_predict = lgb_clf.predict(target[["runnerName_L","prefacture_L"]].values)
target["score"] = y_predict
target["rank"] = target.rank(method="min")["score"]
target[["rank","runnerName","score"]].sort_values("score").to_csv("predict_we.csv",encoding="cp932")

# コースの難易度分布を使った予測
# 男子
#target = pd.read_csv("targetRunnerList_m.csv")
#target["place"] = "[望郷の森]"
#target["runnerName_L"] = runner.transform(target["runnerName"])
#target["place_L"] = place.transform(target["place"])

#course = [20,40,60,80,100,120,140,160,180,200]
#target["score"] = 0

#for i in course:

#	target["difficulty"] = i
#	target["score"] = target["score"] + lgb_clf.predict(target[["runnerName_L","place_L","difficulty"]].values)
	
#target["rank"] = target.rank(method="min")["score"]
#target[["rank","runnerName","score"]].sort_values("score").to_csv("predict_me.csv",encoding="cp932")

# 女子
#target = pd.read_csv("targetRunnerList.csv")
#target["place"] = "[望郷の森]"
#target["runnerName_L"] = runner.transform(target["runnerName"])
#target["place_L"] = place.transform(target["place"])

#course = [20,40,60,80,100,120,140,160,180,200]
#target["score"] = 0

#for i in course:

#	target["difficulty"] = i
#	target["score"] = target["score"] + lgb_clf.predict(target[["runnerName_L","place_L","difficulty"]].values)
	
#target["rank"] = target.rank(method="min")["score"]
#target[["rank","runnerName","score"]].sort_values("score").to_csv("predict_we.csv",encoding="cp932")

