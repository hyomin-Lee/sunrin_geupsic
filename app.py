#-*- coding: utf-8 -*-
from flask import Flask, request

def parse(date):
    f = open('./'+date, "r")
    message = f.readline()
    return message

application = Flask(__name__)
@application.route('/keyboard')
def keyboard():
    key = '{"type":"buttons", "buttons":["오늘의 급식", "내일의 급식"]}'
    return key
@application.route('/message',methods=['POST'])
def message():
    if request.method == "POST":
        select = request.get_json()
        if select['content'] == '오늘의 급식':
            message = parse('today')
            return message
        elif select['content'] == '내일의 급식':
            message = parse('tomorrow')
            return message
if __name__ == '__main__':
    application.run(host='0.0.0.0')
