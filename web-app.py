from flask import Flask, render_template,request,redirect,url_for,session,jsonify
from flask_mysqldb import MySQL
from flask import Flask, render_template, request
import MySQLdb.cursors
import re

app= Flask(__name__)

app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 's7SFf1WE1M'
app.config['MYSQL_PASSWORD'] = 'oKniqLxnwl'
app.config['MYSQL_DB'] = 's7SFf1WE1M'
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('altdesc.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !' 
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('index.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/ProjectDesc')
def ProjectDesc():
    return render_template('desc.html')    
@app.route('/loggedin')
def altindex():
    return render_template('altindex.html')

@app.route('/contactloggedin')
def altcontact():
    return render_template('altcontact.html')

@app.route('/altdesc')
def altDesc():
    return render_template('altdesc.html')


if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 8080)