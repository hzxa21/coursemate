import MySQLdb
from flask import Flask, g
from sae.const import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB

db = MySQLdb.connect(
            MYSQL_HOST,
            MYSQL_USER,
            MYSQL_PASS,
            MYSQL_DB,
            port=int(MYSQL_PORT),
    charset="utf8"
    )
app = Flask(__name__)
SESSION_KEY = 'vkFwRjPgASwNed1sBmXjy+o/OSY0qFsPe1fljeyDE5aSbidWesAp9tNcenWcnmnS'
app.secret_key=SESSION_KEY

@app.before_request
def init():
    g.conn = db
    g.cursor = db.cursor()
import route

if __name__ == '__main__':
    app.run(debug=True)
