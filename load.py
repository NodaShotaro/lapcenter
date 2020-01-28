
import pandas as pd
import re
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.mstats import gmean

from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

def load():

    df = pd.read_csv('csv/join.csv',encoding='utf-8')
    df['date'] = pd.to_datetime(df['date'])

    return df


def load_noleginfo():

    df = pd.read_csv('csv/join.csv',encoding='utf-8')

    # runner.csvのレッグ情報の削除
    df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)

    # leg.csvのレッグ情報の削除
    df.drop(columns=['difficulty','elapsedLength','length','name','to','topAverage','topAverageLapElapsed'],inplace=True)
    df.drop_duplicates(inplace=True)

    # h:mm:ss形式を除去し，mm;ss形式を残すコード
    # df.drop(df[df['lapTime'].str.match('\d:\d\d:\d\d')].index,inplace=True)
    # df['lapTime'] = pd.to_datetime(df['lapTime'],format='%M:%S')

    df['date'] = pd.to_datetime(df['date'])

    return df


def nagoya(df):

    df = df[df['univ'] == '名古屋']
    return df

def make_hist(df,colname,bins):

    discrete = pd.cut(df[colname],bins).value_counts().sort_index()
    disc_ub = []
    for i in discrete.index.tolist():
        print(i)
        disc_ub.append(round(i.right))

    plt.bar(range(0,len(discrete)),discrete.values,tick_label=disc_ub)
    plt.xticks(rotation=70,fontproperties=fp)
    plt.savefig(colname+'_hist.png')
    plt.clf()