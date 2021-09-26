from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re
app = Flask(__name__)

app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tanya23'
app.config['MYSQL_DB'] = 'myu'
