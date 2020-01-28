import requests
import re

from bs4 import BeautifulSoup


# Lapcenterの指定ページにあるイベント、記録のURL一覧の取得
def get_eventlist(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    event_list = []

    t_event_list = soup.find_all('div',class_=re.compile('^event-item'))

    for i in range(len(t_event_list)):

        try:
            event_name = t_event_list[i].find('div',class_=re.compile('^event-name')).string.strip()
            file_list = t_event_list[i].find('div',class_='event-file').find_all('a')

            for j in range(len(file_list)):
                if re.match(r'記録',file_list[j].string):
                    file_url = file_list[j]['href']

                    event_list.append((event_name,file_url))

        except AttributeError:
            continue

    return event_list

# 1-5ページまでのイベント・記録のURL一覧取得
def get_1to5_eventlist():
    event_list = []
    for i in range(1):
        event_list.extend(get_eventlist('https://mulka2.com/lapcenter/?page='+str(i)))
    
    return event_list

# サンプル
url = "https://mulka2.com/lapcenter/lapcombat2/split-list.jsp?event=5447&file=1&class=0&content=analysis"

print(get_1to5_eventlist())
