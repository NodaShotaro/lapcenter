
import pandas as pd

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

def extractTargetRunner(df,filename):

    target_runner = pd.read_csv(filename)["runnerName"]

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
