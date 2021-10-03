from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import pymysql
import re

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.secret_key = 'renthouse123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'houserent_db'

mysql = MySQL(app)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM login WHERE username = %s AND password = %s', (username, password))

        login = cursor.fetchone()

        if login:

            session['login'] = True
            session['username'] = account[username]
            session['password'] = account[password]

            return redirect(url_for('home'))
        else:

            msg = 'Incorrect username/password!'

    return render_template('home.html', msg=msg)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM login WHERE username = %s', (username))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:

            cursor.execute('INSERT INTO login VALUES (NULL, %s, %s, %s, %s)', (username, password))
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('registration.html', msg=msg)


@app.route('/')
def home():
    if 'login' in session:
        return render_template('home.html', username=session['username'])

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)