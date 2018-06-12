#-*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import datetime


key = '"keyboard":{"type":"buttons", "buttons":["오늘의 급식", "내일의 급식"]}}'
output_date = []
def create_form(menu):
    menu = menu.replace('\n', '')
    menu = menu.replace('\r', '')
    menu = menu.replace('\t', '')
    menu = menu.replace(' ', '')
    menu = menu.replace(',', '\\n')
    #menu = menu.replace('(', '\\n')
    #menu = menu.replace(')', '')
    message = '{"message":{"text":' + '\"'+ menu + '\"' + '}' + ',' + key
    return message

def plus_dinner():
    d = datetime.datetime.now()
    weekday = d.weekday()
    weekday = str(weekday)
    if weekday =='6':
        tomorrow_weekday = '0'
        current = datetime.datetime.now()
        tomorrow_d = current + datetime.timedelta(days=3)
        tomorrow_d = str(tomorrow_d)
        tomorrow_d = tomorrow_d[0:10]
        d = tomorrow_d.replace('-','.')
    else :
        tomorrow_weekday = int(d.weekday())+1
        tomorrow_weekday = str(tomorrow_weekday)
        d = str(d)
        d = d[0:10]
        d = d.replace('-','.')

    weekday = weekday.replace('0','월')
    weekday = weekday.replace('1','화')
    weekday = weekday.replace('2','수')
    weekday = weekday.replace('3','목')
    weekday = weekday.replace('4','금')
    weekday = weekday.replace('5','토')
    weekday = weekday.replace('6','일')

    tomorrow_weekday = tomorrow_weekday.replace('0','월')
    tomorrow_weekday = tomorrow_weekday.replace('1','화')
    tomorrow_weekday = tomorrow_weekday.replace('2','수')
    tomorrow_weekday = tomorrow_weekday.replace('3','목')
    tomorrow_weekday = tomorrow_weekday.replace('4','금')
    tomorrow_weekday = tomorrow_weekday.replace('5','토')
    tomorrow_weekday = tomorrow_weekday.replace('6','일')

    req = requests.get('https://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=B100000658&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=3&schYmd=%s' % d)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')

    pars = soup.select('table > tbody > tr > td')


    del pars[0:8]
    del pars[5:]

    pars2 = ''
    for i in range(0,5):
        pars[i] = str(pars[i])
        pars[i] = pars[i].replace('<br/>', '\\n')
        pars[i] = pars[i].replace('.','')
        pars[i] = pars[i]
        for k in range(0,10):
            pars[i] = pars[i].replace(str(k),'')
        pars2 = pars2 + pars[i]

    soup = BeautifulSoup(pars2,'html.parser')
    pars = soup.select('td')


    menu = []
    for i in pars:
        menu.append("\n\n[석식]\\n"+i.text) 

    dic_ = {'월':menu[0],'화':menu[1],'수':menu[2],'목':menu[3],'금':menu[4],'토':'석식이 없습니다.','일':'석식이 없습니다.'}

    today_dinner = dic_[weekday]
    tomorrow_dinner = dic_[tomorrow_weekday]

    return today_dinner, tomorrow_dinner

def check_day():
    date = soup.select('dl > dd > p.date')
    to_day = datetime.datetime.now()
    tomo_day = to_day + datetime.timedelta(days=1)
    tomo_day = str(tomo_day)
    tomo_day = tomo_day[8:10]
    tomo_day = int(tomo_day)

    to_day = str(to_day)
    to_day = to_day[8:10]
    to_day = int(to_day)
    date_list = []
    for day in date:
        output_date.append(day.text)
        date_list.append(int(day.text[8:10]))
    print (tomo_day)
    print (date_list)
    if tomo_day not in date_list :
        tomorrow.write('{"message":{"text":' + '\"' + '내일 급식이 없습니다!' + '\"' + '}' + ',' + key)

    if to_day in date_list :
        return 1;
    else :
        today.write('{"message":{"text":' + '\"' + '오늘 급식이 없습니다!' + '\"' + '}' + ',' + key)
        to_day = int(to_day)
        print ("asaaaaa")
        print (date_list[0])

        if tomo_day != date_list[0]:
            tomorrow.write('{"message":{"text":' + '\"' + '내일 급식이 없습니다!' + '\"' + '}' + ',' + key)
            sys.exit()
        else :
            tomorrow.write(create_form(output_date[0] +'\\n\\n'+'[중식]\\n'+ menu[0].text + '\\n\\n'+tomorrow_dinner))
            sys.exit()            

today = open("/home/packet/sun-rin_geupsic/today", "w")
tomorrow = open("/home/packet/sun-rin_geupsic/tomorrow", "w")
req = requests.get('http://www.sunrint.hs.kr/index.do')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
menu = soup.select(' dl > dd > p.menu')

today_dinner,tomorrow_dinner = plus_dinner()

check_day()
today.write(create_form(output_date[0] + '\\n\\n'+'[중식]\\n' + menu[0].text +'\\n\\n'+ today_dinner ))
tomorrow.write(create_form(output_date[1] + '\\n\\n'+'[중식]\\n'+ menu[1].text +'\\n\\n' +tomorrow_dinner))
