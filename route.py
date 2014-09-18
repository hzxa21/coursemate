#!/usr/bin/env python
# coding=utf-8
from app import app
from flask import g, request, redirect, render_template, session, url_for
import sysujwxt

def query_db(query, args=(), one=False):
    g.cursor.execute(query, args)
    rv = [dict((g.cursor.description[idx][0], value)
        for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv

def fetch_course():
    res, course_info = sysujwxt.get_course(session['USR_COOKIE'],
            '2014-2015', '2')
    if not res:
        session.pop('USR_COOKIE')
        return redirect(url_for('login'))
    else:
        for item in course_info:
            course_item = query_db("SELECT * FROM course WHERE cou_id = %s",
                    (item['cou_id'],), one=True)
            if not course_item:
                sql = """INSERT INTO course (cou_id, course_name, time, teacher)
                VALUES (%s, %s, %s, %s)"""
                g.cursor.execute(sql, (
                    item['cou_id'],
                    item['course_name'],
                    item['time'],
                    item['teacher']
                    ))
            sql = "INSERT INTO stu_course (stu_id, cou_id) VALUES (%s, %s)"
            g.cursor.execute(sql, (session['USR_ID'], item['cou_id']))
        g.conn.commit()
        return course_info

@app.route('/', methods=['GET'])
def index():
    if 'USR_ID' in session:
        return redirect(url_for('course'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        form传值变量名：
            stuid：学号
            password：密码

        返回值：
            error：验证是否出错（True表示出错)
    """
    if request.method == 'POST':    
        res, cookie = sysujwxt.login(request.form['stuid'],
                request.form['password'])
        if res:
            user = query_db("SELECT * FROM student WHERE user_id = %s",
                    (request.form['stuid'],), one=True)
            if user is None:
                res2, info = sysujwxt.get_student_info(cookie)
                if res2:
                    sql = '''INSERT INTO student (user_id, username, school, major,
                    grade) VALUES (%s, %s, %s, %s, %s)'''
                    g.cursor.execute(sql, (
                        request.form['stuid'],
                        info['name'],
                        info['school'],
                        info['major'],
                        info['grade']
                        ))
                    g.conn.commit()
                else:
                    return render_template('login.html', error=True)
            # store user's cookie of sysujwxt
            session['USR_COOKIE'] = cookie;
            session['USR_ID'] = request.form['stuid']
            
            return redirect(url_for('course'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    if 'USR_ID' in session:
        session.pop('USR_ID')
        session.pop('USR_COOKIE')
    return redirect(url_for('login'))

@app.route('/course', methods=['GET', 'POST'])
def course():
    """
        form传值变量名：
            year：学年度
            term：学期

        返回值：
            course_list: 学生课程列表，每个课程为一个字典
    """
    if 'USR_ID' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        sql = '''SELECT * FROM stu_course a, course b WHERE
        a.cou_id = b.cou_id and a.stu_id = %s'''
        course_info = query_db(sql, (session['USR_ID'],))
        if not course_info:
            course_info = fetch_course()
        return render_template('course.html', course_list=course_info)
    else:
        course_info = fetch_course()
        return render_template('course.html', course_list=course_info)

@app.route('/user', methods=['GET', 'POST'])
def user():
    """
        form传值变量名：
            email,call,signature,mail,pre_school,address,detail_address,nickname

        返回值：
            user_info: 用户个人信息的字典
    """
    if 'USR_ID' in session:
        if request.method == 'GET':
            user_info = query_db("SELECT * FROM student WHERE user_id = %s",
                    (session['USR_ID'],), one = True)
            return render_template('user.html', user_info=user_info)
        else:
           if g.cursor.execute("""UPDATE SET nickname = %s, email = %s,
               mail = %s, call = %s, signature = %s, pre_school = %s,
               address = %s, detail_address = %s""", (
                   request.form['nickname'],
                   request.form['email'],
                   request.form['mail'],
                   request.form['call'],
                   request.form['signature'],
                   request.form['pre_school'],
                   request.form['address'],
                   request.form['detail_address']
                   )):
               g.conn.commit()
               return redirect(url_for('user'))
           else:
               return render_template('user.html', error=True)
    else:
        return redirect(url_for('login'))

@app.route('/course/<course_id>', methods=['GET', 'POST'])
def course_page(course_id):
    """
        form传值变量名：
            title:标题
            content:内容

        返回值：
            post_list: 课程帖子列表，每一个帖子是一个字典
    """
    if 'USR_ID' in session:
        if request.method == 'GET':
            post_info = query_db('''SELECT * FROM post a, student b WHERE
            a.author_id = b.user_id and cou_id = %s''', (course_id,))
            return render_template('course_page.html',
                    post_list=post_info, cou_id=str(course_id))
        else:
            g.cursor.execute('''INSERT INTO post (cou_id, title, content,
            author_id) VALUES (%s, %s, %s, %s)''', (
                course_id,
                request.form['title'],
                request.form['content'],
                session['USR_ID']
                ))
            g.conn.commit()
            return redirect('/course/' + course_id)
    else:
        return redirect(url_for('login'))

@app.route('/course/<course_id>/post')
def post(course_id):
    if 'USR_ID' in session:
        return render_template('post.html', cou_id=course_id)

@app.route('/discussion/<discussion_id>/post')
def comment(discussion_id):
    if 'USR_ID' in session:
        return render_template('comment.html', post_id=discussion_id)

@app.route('/discussion/<discussion_id>', methods=['GET', 'POST'])
def discussion_page(discussion_id):
    """
        form传值变量名：

        返回值：
            comment_list: 帖子评论列表，每一个评论是一个字典
    """
    if 'USR_ID' in session:
        if request.method == 'GET':
            comment_info = query_db('''SELECT * FROM comments a, student b WHERE
            a.author_id = b.user_id and post_id = %s''', (discussion_id,))
            post_info = query_db('''SELECT * FROM post a, student b WHERE
            a.author_id = b.user_id and post_id = %s''',
            (discussion_id,), one=True)
            return render_template('discussion_page.html',
                    comment_list=comment_info,
                    post_info=post_info,
                    post_id=discussion_id
                    )
        else:
            g.cursor.execute('''INSERT INTO comments (post_id, content,
            author_id) VALUES (%s, %s, %s)''', (
                discussion_id,
                request.form['content'],
                session['USR_ID']
                ))
            g.conn.commit()
            return redirect('/discussion/' + str(discussion_id))
    else:
        return redirect(url_for('login'))
