#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import pycurl
import re
import StringIO
import json
import logging
import sys

LOGIN_TIMEOUT = 15
REQUEST_TIMEOUT = 25

# ----------------
# Basic functions
# ----------------
def format_to_json(unformated_json):
    # pat = r'(\w+(?=:))'
    pat = r'((?:(?<=[,{\[])\s*)(\w+)(?=:))'
    sub = r'"\1"'
    return re.sub(pat, sub, unformated_json)

def retrive_data(url, cookie, request_json):
    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, url)
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.POSTFIELDS, request_json)
    ch.setopt(pycurl.TIMEOUT, REQUEST_TIMEOUT)
    ch.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data', 'render: unieap'])
    ch.setopt(pycurl.COOKIE, "JSESSIONID="+cookie)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)

    try:
        ch.perform()
    except pycurl.error, e:
        logging.error('%s, %s', e[0], e[1])
        return (False, 'timeout')

    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ret_body = ret.getvalue()
    ch.close()
    if (ret_body.startswith('THE-NODE-OF-SESSION-TIMEOUT', 5)):
        return (False, 'expired')
    else:
        return (True, ret_body)

def login(username, passward):
    url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'

    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, url)
    ch.setopt(pycurl.TIMEOUT, LOGIN_TIMEOUT)
    ch.setopt(pycurl.POST, True)
    data = urllib.urlencode({'j_username': username, 'j_password': passward})
    ch.setopt(pycurl.POSTFIELDS, data)
    ret = StringIO.StringIO()
    ch.setopt(pycurl.WRITEFUNCTION, ret.write)
    # add header to ret value
    ch.setopt(pycurl.HEADER, True)

    try:
        ch.perform()
    except pycurl.error, e:
        logging.error('%s, %s', e[0], e[1])
        return (False, 'timeout')

    ret_code = ch.getinfo(pycurl.HTTP_CODE)
    ch.close()
    if ret_code == 200:
        logging.debug('Login errorpass: %s %s', username, passward)
        return (False, 'errorpass')
    else:
        ret_header = ret.getvalue()
        cookies = re.findall(r'^Set-Cookie: (.*);', ret_header, re.MULTILINE)
        cookie = cookies[0][11:]
        logging.debug('Login success: %s %s', username, passward)
        return (True, cookie)

def get_course_result(cookie,year,term):
    url = 'http://uems.sysu.edu.cn/jwxt/xstk/xstk.action?method=getXsxkjgxxlistByxh '
    query_json = '''
    {
    "header": {
        "code": -100, 
        "message": {
            "title": "", 
            "detail": ""
        }
    }, 
    "body": {
        "dataStores": {
            "xsxkjgStore": {
                "rowSet": {
                    "primary": [ ], 
                    "filter": [ ], 
                    "delete": [ ]
                }, 
                "name": "xsxkjgStore", 
                "pageNumber": 1, 
                "pageSize": 20, 
                "recordCount": 62, 
                "rowSetName": "pojo_com.neusoft.education.sysu.xk.xkjg.entity.XkjgxxEntity", 
                "order": "xkjg.xnd desc,xkjg.xq desc, xkjg.jxbh"
            }
        }, 
        "parameters": {
            "xsxkjgStore-params": [
                {
                    "name": "Filter_xkjg.xnd_0.9842467070587848", 
                    "type": "String", 
                    "value": "'%s'", 
                    "condition": " = ", 
                    "property": "xkjg.xnd"
                }, 
                {
                    "name": "Filter_xkjg.xq_0.30827901561365295", 
                    "type": "String", 
                    "value": "'%s'", 
                    "condition": " = ", 
                    "property": "xkjg.xq"
                }
            ], 
            "args": [ ]
        }
    }
    }
    '''%(year,term)
    return retrive_data(url, cookie, query_json)

# --------------------
# Personal info Query
# --------------------
def get_info(cookie):
    logging.debug('Getting info: %s', cookie)
    url = "http://uems.sysu.edu.cn/jwxt/WhzdAction/WhzdAction.action?method=getGrwhxxList"
    query_json = """
    {
        header: {
            "code": -100,
            "message": {
                "title": "",
                "detail": ""
            }
        },
        body: {
            dataStores: {
                xsxxStore: {
                    rowSet: {
                        "primary": [],
                        "filter": [],
                        "delete": []
                    },
                    name: "xsxxStore",
                    pageNumber: 1,
                    pageSize: 10,
                    recordCount: 0,
                    rowSetName: "pojo_com.neusoft.education.sysu.xj.grwh.model.Xsgrwhxx"
                }
            },
            parameters: {
                "args": [""]
            }
        }
    }
    """
    return retrive_data(url, cookie, query_json)

# --------------------
# Personal info Query
# --------------------
def get_info(cookie):
    logging.debug('Getting info: %s', cookie)
    url = "http://uems.sysu.edu.cn/jwxt/WhzdAction/WhzdAction.action?method=getGrwhxxList"
    query_json = """
    {
        header: {
            "code": -100,
            "message": {
                "title": "",
                "detail": ""
            }
        },
        body: {
            dataStores: {
                xsxxStore: {
                    rowSet: {
                        "primary": [],
                        "filter": [],
                        "delete": []
                    },
                    name: "xsxxStore",
                    pageNumber: 1,
                    pageSize: 10,
                    recordCount: 0,
                    rowSetName: "pojo_com.neusoft.education.sysu.xj.grwh.model.Xsgrwhxx"
                }
            },
            parameters: {
                "args": [""]
            }
        }
    }
    """
    return retrive_data(url, cookie, query_json)

def get_course(cookie,year,term):
#获取学生课程，返回课程列表，每个课程为一个字典
    result = get_course_result(cookie.encode('ascii'),year.encode('ascii'),term.encode('ascii'))
    if result[0] == True:
        result = format_to_json(result[1])
        data = json.loads(result)
        data = data['body']['dataStores']['xsxkjgStore']['rowSet']['primary']
        course = []
        i = 0
        for item in data:
            #print item
            one = dict()
            one['id'] = item['resourceID']
            one['coursename'] = item['kcmc']
            one['teacher'] = item['xm'].split(',')[0]
            one['time'] = item['sksjdd']
            course.append(one)
        return (True,course)
    else:
        return (False,None)

def get_student_info(cookie):
#获取学生个人信息
    result = get_info(cookie)
    if result[0] == True:
        result = format_to_json(result[1])
        data = json.loads(result)
        data = data['body']['dataStores']['xsxxStore']['rowSet']['primary'][0]
        info = dict()
        info['stuID'] = data['xh']      #学号
        info['name'] = data['xm']       #姓名
        info['school'] = data['xymc']   #学院
        info['major'] = data['zyfxmc']  #专业
        info['grade'] = data['njmc']     #年级
        return (True,info)
    else:
        return (False,None)

#测试
if __name__ == "__main__":
    username = sys.argv[1] #用户名
    password = sys.argv[2] #密码
    res, cookie = login(username, password)

    if res:
        year = '2013-2014' #学期
        term = '2'  #第几学期，1，2, 3
        result = get_course(cookie,year,term)
        if result[0] == True:
            result = result[1];
            for course in result:
                print 'The course ID : %s' % course['id']
                print 'The course name: %s' % course['coursename']
                print 'The Teacher is : %s' % course['teacher']
                print 'The time is : %s ' % course['time']
                print '\n'
        else:
            print('course error')

        result = get_student_info(cookie)
        if result[0] == True:
            result = result[1]
            print result['stuID']
            print result['name']
            print result['grade']
            print result['school']
            print result['major']
        else:
            print 'get info error'

    else:
        print('login error')

