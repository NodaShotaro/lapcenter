import mylib

import pandas as pd
import lightgbm as lgb
import math

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def smoothing(cnt,score,average_score,alpha=0.1):
	return (1-(math.e)**((-alpha)*cnt)) * score + ((math.e)**((-alpha)*cnt)) * average_score

def makeEncoder(df,dimName):

	enc = LabelEncoder()
	enc = enc.fit(df[dimName])
	return enc

def makeTrainDataQuery(df,dimName):

	query = []
	lst = pd.DataFrame()
	for i,t in df.groupby(dimName):
		print(i)
		query.append(t[dimName].count())
		lst = pd.concat([lst,t])
	
	return lst,query

def trainLambdaRank(lgtrain,lgvalid,cf):

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
		categorical_feature=cf,
		num_boost_round=100,
		valid_sets=[lgtrain, lgvalid],
		valid_names=['train','valid'],
		verbose_eval=1
	)

	return lgb_clf


df = mylib.load()
df = df[~(df["eventName"] == "第16回東海学生オリエンテーリング選手権大会")]

runner = makeEncoder(df,"runnerName")
df["runnerName_L"] = runner.transform(df["runnerName"])

place = makeEncoder(df,"prefacture")
df["prefacture_L"] = place.transform(df["prefacture"])

df["race"] = df["eventName"] + df["classId"].astype(str) +"-"+ df["from"].astype(str)
event = makeEncoder(df,"race")
df["race_L"] = event.transform(df["race"])

valid = df[df["date"].dt.month == 2]
df = df[~(df["date"].dt.month == 2)]

df,query = makeTrainDataQuery(df,"race_L")
valid,query_v = makeTrainDataQuery(valid,"race_L")

#query = (df.groupby("race_L").count())["eventName"].values
#query_v = (valid.groupby("race_L").count())["eventName"].values

# 特徴つき
lgtrain = lgb.Dataset(df[["runnerName_L","prefacture_L"]].values, df["lapRank"].values, categorical_feature=[0,1],group=query)
lgvalid = lgb.Dataset(valid[["runnerName_L","prefacture_L"]].values, valid["lapRank"].values, categorical_feature=[0,1],group=query_v)
lgb_hasFeature = trainLambdaRank(lgtrain,lgvalid,[0,1])


# 特徴なし（全体の平均値）
lgtrain = lgb.Dataset(df[["runnerName_L"]].values, df["lapRank"].values, categorical_feature=[0],group=query)
lgvalid = lgb.Dataset(valid[["runnerName_L"]].values, valid["lapRank"].values, categorical_feature=[0],group=query_v)
lgb_all = trainLambdaRank(lgtrain,lgvalid,[0])


# 予測用コード
# 男子の予想
target = pd.read_csv("targetRunnerList_m.csv")
target["prefacture"] = "栃木"
target["runnerName_L"] = runner.transform(target["runnerName"])
target["prefacture_L"] = place.transform(target["prefacture"])

# 栃木での出走回数の導出
df_men = mylib.extractTargetRunner(df,target)
df_race_cnt_all = (df_men.groupby("runnerName").count())["race_L"]

df_men = df_men[df_men["prefacture"] == "栃木"]
df_race_cnt = (df_men.groupby("runnerName").count())["eventName"]

target = pd.merge(target,df_race_cnt_all,how="left",left_on="runnerName",right_index=True)
target = pd.merge(target,df_race_cnt,how="left",left_on="runnerName",right_index=True)
target["eventName"].fillna(0,inplace=True)
target["race_L"].fillna(0,inplace=True)

y_predict = lgb_hasFeature.predict(target[["runnerName_L","prefacture_L"]].values)
y_average = lgb_all.predict(target[["runnerName_L"]].values)

alpha = 0.1
alpha_all = 0.07

target["score_raw"] = y_predict
target["score_avg"] = y_average
target["score1"] = (1-(math.e)**((-alpha)*target["eventName"])) * target["score_raw"] + ((math.e)**((-alpha)*target["eventName"])) * target["score_avg"]
target["score2"] = (1-(math.e)**((-alpha_all)*target["race_L"])) * target["score1"]

target["rank"] = target.rank(method="min")["score2"]
target[["rank","runnerName","score2","score1","score_raw","score_avg","eventName","race_L"]].sort_values("score2").to_csv("predict/predict_me.csv",index=False)

#女子の予想
#target = pd.read_csv("targetRunnerList.csv")
#target["prefacture"] = "愛知"
#target["runnerName_L"] = runner.transform(target["runnerName"])
#target["prefacture_L"] = place.transform(target["prefacture"])

#y_predict = lgb_clf.predict(target[["runnerName_L","prefacture_L"]].values)
#target["score"] = y_predict
#target["rank"] = target.rank(method="min")["score"]
#target[["rank","runnerName","score"]].sort_values("score").to_csv("predict/predict_we.csv")


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

