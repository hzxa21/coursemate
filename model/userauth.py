#!/usr/bin/env python
# coding=utf-8
from flask import abort,request, jsonify,g,session
from model import app
from api import sysucourse

@app.route('/login',method = ['GET','POST'])
def login():
    if request.method == 'POST':    
        res, cookie = sysucourse.login(request.form['username'],request.form['password'])
        if res:
            if not g.cursor.execute(
                "SELECT 'cookie' FROM 'users' WHERE 'username' = %s",request.form['username']
                ):
                g.cursor.execute(
                    "UPDATE 'users' SET 'cookie' = %s WHERE 'username' = %s",
                    cookie,request.form['username'])
            else:
                g.cursor.execute(
                    "INSERT INTO users(username.cookie) VALUES (%s,%s)",
                    request.form['username'],cookie)
            g.conn.commit()

            session['USERNAME'] = request.form['username'];
        else:
            abort(403)
    else:


