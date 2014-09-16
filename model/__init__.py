import MySQLdb
from sae.const import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
from flask import Flask, g
app  = Flask(__name__); 
db = MySQLdb.connect(
        MYSQL_HOST,
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_DB,
        port=int(MYSQL_PORT)
        )
g.conn = db;
g.cursor = db.cursor;
