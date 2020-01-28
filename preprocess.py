
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# 出走人数 min_sample未満のレース結果を削除

def filter_little_race(data,min_sample):

    df = data.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'])
    df.drop_duplicates(inplace=True)

    counts = df.groupby(['eventName','classId']).count()['clubName']

    delete_list = counts[counts < min_sample].index

    for i in delete_list.tolist():
        del_l = data['eventName'] == i[0]
        del_r = data['classId'] == i[1]
        data = data[~(del_l & del_r)]
    
    return data

# 特徴量：大学名，学年の生成
def make_univ_grade(data):

    univList = data.query('clubName.str.match(".*大学[0-9]") ')[['runnerName','clubName']].drop_duplicates()

    univ_grade = univList['clubName'].str.split('大学',expand=True)
    univ_grade.rename(columns={0:'univ',1:'grade'},inplace=True)

    univList = univList.join(univ_grade)
    ex = univList.groupby('runnerName').max()

    ex.drop('clubName',axis=1,inplace=True)
    out = pd.merge(data,ex,on='runnerName',how='left')

    return out

def convertLapTime(df,dimName):

    df[dimName].replace("X","23:59:59",inplace=True)

    hour_scale = df[df[dimName].str.match("^\d+:\d\d:\d\d$")]
    min_scale = df[df[dimName].str.match("^\d+:\d\d$")]

    minus_scale = df[df[dimName].str.match("^-\d+:\d\d$")]

    ans = []

    if len(min_scale) > 0:
        min_scale.loc[:,dimName+"N"] = pd.to_datetime(min_scale[dimName],format="%M:%S")
        min_scale.loc[:,dimName+"N"] = min_scale.loc[:,dimName+"N"].dt.minute * 60 + min_scale.loc[:,dimName+"N"].dt.second

        min_scale.drop(columns=dimName,inplace=True)
        min_scale.rename(columns = {dimName+"N" : dimName},inplace=True)
        ans.append(min_scale)

    if len(hour_scale) > 0:
        hour_scale.loc[:,dimName+"N"] = pd.to_datetime(hour_scale[dimName],format="%H:%M:%S")
        hour_scale.loc[:,dimName+"N"] = hour_scale.loc[:,dimName+"N"].dt.hour * 3600 + hour_scale.loc[:,dimName+"N"].dt.minute * 60 + hour_scale.loc[:,dimName+"N"].dt.second

        hour_scale.drop(columns=dimName,inplace=True)
        hour_scale.rename(columns = {dimName+"N" : dimName},inplace=True)
        ans.append(hour_scale)

    if len(minus_scale) > 0:
        minus_scale.loc[:,dimName+"N"] = pd.to_datetime(minus_scale[dimName],format="-%M:%S")
        minus_scale.loc[:,dimName+"N"] =  - minus_scale.loc[:,dimName+"N"].dt.minute * 60 - minus_scale.loc[:,dimName+"N"].dt.second

        minus_scale.drop(columns=dimName,inplace=True)
        minus_scale.rename(columns = {dimName+"N" : dimName},inplace=True)
        ans.append(minus_scale)

    return pd.concat(ans)

def join_with_leginfo(data):

    leg = pd.read_csv('csv/leg_concat.csv',encoding='utf-8')
    df = pd.merge(data,leg,on=['classId','eventName','from'])

    return df

def makeStartPosition(df):

    ans = []

    df["start"] = pd.to_datetime(df["start"])
    df["start_pos"] = df["start"].dt.minute + df["start"].dt.hour * 60

    x = df.groupby(["eventName","classId"]).min()["start_pos"]

    for i,t in df.iterrows():
        t["start_pos"] = t["start_pos"] - x[t["eventName"],t["classId"]]
        ans.append(t)

    return pd.DataFrame(ans)

data = pd.read_csv('csv/runner_concat.csv',encoding='utf-8')

# 所属の欠損を補完
data['clubName'].fillna('N',inplace=True)
data = filter_little_race(data,6)
data = make_univ_grade(data)

data['lapTime'].fillna("X",inplace=True)
data = convertLapTime(data,"lapTime")

data['legLossTime'].fillna("X",inplace=True)
data = convertLapTime(data,"legLossTime")

data['result'].fillna("X",inplace=True)
data['result'].replace("DISQ","X",inplace=True)
data['result'].replace("DNF","X",inplace=True)
data['result'].replace("DNS","X",inplace=True)
data['result'].replace("?","X",inplace=True)
data['result'].replace("ECL","X",inplace=True)
data[data["result"].str.match("^P")]["result"] = "X"

data = convertLapTime(data,"result")

data = makeStartPosition(data)

data = join_with_leginfo(data)

data.to_csv('csv/join.csv',encoding='utf-8',index=False)
