#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import json
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

def retrive_data(url,cookie, request_json):

    cookie = 'JSESSIONID='+cookie

    #设置 cookie 处理器
    #cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    opener.addheaders.append(('Cookie',cookie))

    request = urllib2.Request(url,request_json)
    request.add_header('Content-Type','multipart/form-data')
    request.add_header('render','unieap')

    try:
        response = urllib2.urlopen(request,timeout=REQUEST_TIMEOUT)
    except:
        return (False, 'timeout')

    ret_code = response.getcode()

    ret_body = response.read()

    return (True, ret_body)

def login(username, passward):
    url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'

    #设置 cookie 处理器
    cj = cookielib.LWPCookieJar()
    #cj = cookielib.CookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


    postData = urllib.urlencode({'j_username': username, 'j_password': passward})

    request = urllib2.Request(url,postData)

    try:
        response = urllib2.urlopen(request,timeout=LOGIN_TIMEOUT)
    except:
        return (False, 'timeout')

    ret_code = response.getcode()

    ret_body = response.read()

    cookie = ""

    for item in cj:
        if item.name == 'JSESSIONID':
            cookie = item.value
            break
        else:
            cookie = "error"

    if cookie == 'error':
        return (False,'errorpass')

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
            one['cou_id'] = item['jxbh']
            one['course_name'] = item['kcmc']
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
        info['sex'] = data['xbm']       #可能为性别
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
                print 'The course ID : %s' % course['cou_id']
                print 'The course name: %s' % course['course_name']
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
        print cookie

