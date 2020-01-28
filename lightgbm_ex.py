import load 

import pandas as pd
import lightgbm as lgb

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

df = load.load_noleginfo()
df.dropna(subset=["runnerName"],inplace=True)
df = df[(df["rank"] != "参") & (df["rank"] != "代")]
df.fillna({"place" : "Empty", "clubName": "Empty"},inplace=True)


runner = LabelEncoder()
runner = runner.fit(df["runnerName"])
df["runnerName_L"] = runner.transform(df["runnerName"])

club = LabelEncoder()
club = club.fit(df["clubName"])
df["clubName_L"] = club.transform(df["clubName"])

place = LabelEncoder()
place = place.fit(df["place"])
df["place_L"] = place.transform(df["place"])

df["race_L"] = df["eventName"] + df["classId"].astype(str)
event = LabelEncoder()
event = event.fit(df["race_L"])
df["race_L"] = event.transform(df["race_L"])

df["month"] = df["date"].dt.month

valid = df[(df["eventName"] == "第44回全日本オリエンテーリング大会") | (df["eventName"] == "All Japan Orienteering Championships 2019 - Long Distance")]
df = df[~((df["eventName"] == "第44回全日本オリエンテーリング大会") | (df["eventName"] == "All Japan Orienteering Championships 2019 - Long Distance"))]
valid = df
query = df.groupby("race_L").count()
query_v = valid.groupby("race_L").count()

lgtrain = lgb.Dataset(df[["runnerName_L","place_L"]].values, df["rank"].values, categorical_feature=[0,1],group=query["runnerName"])
lgvalid = lgb.Dataset(valid[["runnerName_L","place_L"]].values, valid["rank"].values, categorical_feature=[0,1],group=query_v["runnerName"])

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
	num_boost_round=10,
	valid_sets=[lgtrain, lgvalid],
	valid_names=['train','valid'],
	early_stopping_rounds=2,
	verbose_eval=1
)

target = pd.read_csv("targetRunnerList.csv")
target["clubName"] = target["clubName"]+"大学"
target["place"] = "[椛の湖]"
target["month"] = 11
target["runnerName_L"] = runner.transform(target["runnerName"])
target["clubName_L"] = club.transform(target["clubName"])
target["place_L"] = place.transform(target["place"])

y_predict = lgb_clf.predict(target[["runnerName_L","place_L"]].values)

target["score"] = y_predict

print(target[["score","runnerName"]].sort_values("score"))