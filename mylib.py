
import pandas as pd

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

    leg = pd.read_csv('csv/leg.csv',encoding='utf-8')
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

# 各次元の欠損値を補完
def completeMissValue(data):

    data['clubName'].fillna('N',inplace=True)
    data['lapTime'].fillna("X",inplace=True)
    data['legLossTime'].fillna("X",inplace=True)
    data['result'].fillna("X",inplace=True)
    data['result'].replace("DISQ","X",inplace=True)
    data['result'].replace("DNF","X",inplace=True)
    data['result'].replace("DNS","X",inplace=True)
    data['result'].replace("?","X",inplace=True)
    data['result'].replace("ECL","X",inplace=True)
    data[data["result"].str.match("^P")]["result"] = "X"

    return data

# 出走回数min_sample以下のランナーのデータを削除
def delete_little_runner(df,min_sample,leginfo=True):

    if(leginfo):    
        # runner.csvのレッグ情報の削除
        tmp = df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'])

        # leg.csvのレッグ情報の削除
        tmp.drop(columns=['difficulty','elapsedLength','length','name','to','topAverage','topAverageLapElapsed'],inplace=True)
        tmp.drop_duplicates(inplace=True)

        min_sample = 3
        counts = tmp['runnerName'].value_counts()
        delete_list = counts[counts < min_sample].index

        for i in delete_list:
            df = df[df['runnerName'] != i]

    else:
        counts = df['runnerName'].value_counts()
        delete_list = counts[counts < min_sample].index

        for i in delete_list:
            df = df[df['runnerName'] != i]
        
    return df

def extractTargetRunner(df,runnerList_df):

    target_runner = runnerList_df["runnerName"]

    delete_list = []

    for row in df.itertuples():
            
            flag = True
            for target_name in target_runner:
                    if(target_name == row.runnerName):
                            flag = False
            if flag:
                    delete_list.append(row[0])

    target_list = df.drop(delete_list)

    return target_list

# year年 month月以降のデータを抽出
def extractByDate(df,year,month):

    return df[(df["date"].dt.year > year) | ((df["date"].dt.year == year) & (df["date"].dt.month >= month))]

def makeLegLabel(df):

    # clean     : 30秒以下
    # little    : 1分以下
    # miss      : 3分以下
    # big_miss  : 5分以下
    # loss      : 10分以下
    # distress  : 10分以上

    clean = "A"
    little = "B"
    miss = "C"
    big_miss = "D"
    loss = "E"
    distress = "F"
    noexist = "P"

    df["legJudge"] = ""

    df.loc[(df["legLossTime"] > 600),"legJudge"] = distress
    df.loc[(df["legLossTime"] == 86399),"legJudge"] = noexist
    df.loc[(df["legLossTime"] > 300) & (df["legLossTime"] <= 600),"legJudge"] = loss
    df.loc[(df["legLossTime"] > 180) & (df["legLossTime"] <= 300),"legJudge"] = big_miss
    df.loc[(df["legLossTime"] > 90 ) & (df["legLossTime"] <= 180),"legJudge"] = miss
    df.loc[(df["legLossTime"] > 30 ) & (df["legLossTime"] <= 90 ),"legJudge"] = little
    df.loc[(df["legLossTime"] <= 30),"legJudge"] = clean

    return df    

def load():

    df = pd.read_csv('csv/addPrefacture.csv',encoding='utf-8')
    df.dropna(subset=["runnerName"],inplace=True)
    df.fillna({"place" : "Empty","prefacture" : "Empty", "clubName": "Empty"},inplace=True)

    df['date'] = pd.to_datetime(df['date'])

    return df
