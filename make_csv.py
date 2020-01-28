import re
import requests
import csv
import  json
import pandas as pd
from bs4 import BeautifulSoup

# ['a','b','c'] のパース
#
def parse_txt_arr(txt):

    lparam = txt.find('[')
    rparam = txt.rfind(']')

    ans = txt[lparam+1:rparam].replace('\'','').split(',')
    return ans

# runner -> json
# ラップ解析のページを入力
def lap2json(url):

    ans = {}

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    script_list = soup.find_all('script')
    script = script_list[len(script_list)-1].text

    tmp = re.search('.*classId.*',script)
    class_id = tmp.group(0).split(' ')[3].replace(';\r','')

    raw_runner_list = parse_runner(script)
    extend_runner_list = extend_runner_by_leg(raw_runner_list)
    leg_list = parse_leg(script)

    if len(leg_list) == 0:
        return ans

    ans['classId'] = class_id
    ans['runnerList'] = extend_runner_list
    ans['legList'] = leg_list

    return ans

def parse_runner(script):

    data = re.findall('runnerData\[.*=.*',script)
    flag = True

    runner_list = []
    runner = {}

    for i in range(len(data)):
        if(re.match('.*index',data[i])):
            if(flag):           
                flag = False
                continue
            runner_list.append(runner)
            runner = {}
            continue
            
        elif(re.match('.*\[.*\[.*',data[i])):

            lst = data[i].split('\'')
            arr = parse_txt_arr(data[i].split('=')[1])
            runner[lst[1]] = arr

        else:
            lst = data[i].replace(' ','').split('\'')
            runner[lst[1]] = lst[3]
    runner_list.append(runner)

    return runner_list

# runner : 
# lap : [,,,,,] <- 可変長
# losstime : [,,,] <- 長さはそろっている

def extend_runner_by_leg(runnerList):

    if len(runnerList) <= 0:
        return runnerList
    elif len(runnerList[0]) <= 0:
        return runnerList

    leg_cnt = len(runnerList[0]['lapTime'])
    leg_list = []

    list_attr = []

    for k in runnerList[0]:
        if(isinstance(runnerList[0][k],list)):
            list_attr.append(k)

    for r in runnerList:
        extend_list = {}

        for a in list_attr:
            extend_list[a] = r[a]

        for i in range(0,leg_cnt):
            new_r = r.copy()
            for a in list_attr:
                new_r[a] = extend_list[a][i]
            new_r['from'] = i

            leg_list.append(new_r)

    return leg_list

def parse_leg(script):
    
    data = re.findall('legData\[.*=.*',script)

    leg_list = []
    leg = {}
    flag = True

    if len(data) < 10:
        print(data)
        return leg_list

    for i in range(len(data)):
        if(re.match('.*index',data[i])):
            if(flag):
                flag = False
                continue
            leg_list.append(leg)
            leg = {}
            continue
            
        elif(re.match('.*\[.*\[.*',data[i])):

            lst = data[i].split('\'')
            arr = parse_txt_arr(data[i].split('=')[1])
            leg[lst[1]] = arr

        else:
            lst = data[i].replace(' ','').split('\'')
            if(len(lst) > 3):
                leg[lst[1]] = lst[3]
            else:
                num = data[i].replace(';\r','').split(' ')[2]
                leg[lst[1]] = num
                
    return leg_list

def extract_lap_url(domain,url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')

    tag_list = soup.find_all('a',text='ラップ解析')
    url_list = []

    for tag in tag_list:
        if tag["href"] != "split-list.jsp?event=5653&file=1&class=16&content=analysis":
            url_list.append(domain + tag['href'])

    return url_list

def extract_date(domain,url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')

    span_list = soup.find_all('span')

    date_original = span_list[1].text
    date = date_original.split(' ')[0]

    place = span_list[2].text
    if 'LapCombat2用ファイル' in place:
        place = ''
    elif "公式サイト" in place:
        place = ''

    return (date,place)


def get_title(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')

    return soup.find('title').text

# eventのページに載っている全データの抽出
def extract_event(event_url):

    runnerTable = []
    legTable = []

    domain = "https://mulka2.com/lapcenter/lapcombat2/"
    url_list = extract_lap_url(domain,event_url)
    dateplace = extract_date(domain,event_url)

    class_list = []

    eventName = get_title(event_url)


    for u in url_list:
    
        tmp = lap2json(u)
        if(len(tmp) == 0):
            continue

        class_id = tmp['classId']
        runnerList = tmp['runnerList']
        legList = tmp['legList']

        if class_id == 'null':
            continue

        for r in runnerList:
            r['classId'] = class_id
            r['eventName'] = eventName
            r['date'] = dateplace[0]
            r['place'] = dateplace[1]
            runnerTable.append(r)
        for l in legList:
            l['classId'] = class_id
            l['eventName'] = eventName
            legTable.append(l)
        
    return (runnerTable,legTable)


# --- main -- 

domain = "https://mulka2.com/lapcenter/lapcombat2/"

url_list = []
eventList_checked = []

# raceList_readedからURLをロード
with open("csv/raceList.csv",encoding='utf-8') as f:
    eventList= csv.reader(f,delimiter=",",doublequote=True)

    for t in eventList:
        eventList_checked.append(t)

# raceListからURLをロード
with open("raceList.csv",encoding='utf-8') as f:
    eventList = csv.reader(f,delimiter=",",doublequote=True)

    for t in eventList:
        unchecked = True
        
        for e in eventList_checked:
            if(e[1] == t[1]):
                unchecked = False
        
        if(unchecked):
            url_list.append(t[1])
            eventList_checked.append(t)

lst = []
runnerTable = []
legTable = []

# 各URLをスクレイピングして，ランナーデータ，レッグデータを抽出
for url in url_list:
    print(url)
    tmp = extract_event(url)
    runnerTable.extend(tmp[0])
    legTable.extend(tmp[1])


# 文字列の半角スペース，全角スペースの排除
df = pd.DataFrame(runnerTable)
df.replace(' ','',inplace=True)
df.replace('　','',inplace=True)
df.to_csv("csv/runner_tmp.csv",encoding="utf-8",index=False)


# レッグ番号の△を排除
df_lap = pd.DataFrame(legTable)
df_lap.replace('△',0,inplace=True)
df_lap.to_csv("csv/leg_tmp.csv",encoding="utf-8",index=False)

# レースリストの格納
df_raceList = pd.DataFrame(eventList_checked)
df_raceList.to_csv("csv/raceList.csv",encoding="utf-8",index=False)

#with open(filename,"w") as f:
#    json.dump(runnerTable,f,indent=4,ensure_ascii=False)