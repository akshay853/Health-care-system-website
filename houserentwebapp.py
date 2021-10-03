#import MySQLdb
from flask import Flask, request, session, redirect, url_for, render_template
from flask.templating import render_template_string
from flaskext.mysql import MySQL
import pymysql
import re
# import mysql.connector
from flask_session import Session
from pymysql import cursors
from werkzeug.utils import html


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = 'spare'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root1'
app.config['MYSQL_DATABASE_DB'] = 'houserent_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def mainhome():
    return render_template('/Mainhome.html')

@app.route('/userhome')
def userhome(charset='utf-8'):
    return render_template('user_home.html')

@app.route('/logout')
def logout():
    session.clear
    session['id'] = ""
    return render_template('/Mainhome.html')

@app.route('/loginpage')
def loginpage():
    return render_template('/login.html')


@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST': #and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user_reg WHERE name = %s AND password = %s', (username, password))
        login = cursor.fetchone()
        print(login)
        if login:
            session['login'] = True
            session['id'] = login['user_id']
            session['username'] = login['name']
            options = login['options']
            if options == "admin":
                # session['id'] = "ii"
                # return render_template("adminhome.html")
                adminhome()
                return render_template("adminhome.html")
                #return redirect(url_for(adminhome))
            elif options == "owner":
                # session['id'] = "ii"
                # return render_template("clienthome.html")
                clienthome()
                return render_template("ownerhome.html")
            elif options == "user":
                userhome()
                return render_template("user_home.html")
                #return 
        else:
            return '''<script>alert("invalid User");window.location="/"</script>'''
    else:

        return redirect(url_for('mainhome'))
        return '''<script>alert("Not a user...Please Sign up...!!!");window.location="/"</script>'''


    # return render_template('login.html', msg=msg)
@app.route('/userRegPage')
def userRegPage():
    return render_template('registration.html')


@app.route('/userreg',methods = ['GET','POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST': #and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['userid']
        name = request.form['username']
        address = request.form['address']
        phone_no = request.form['phonenumber']
        password = request.form['pass']
        options = request.form['user']
        cursor.execute('SELECT * FROM user_reg WHERE name = %s',name)
        user_reg = cursor.fetchone()
        if user_reg:
            msg = 'Account already exists!'
            return '''<script>alert("Account already exists!");window.location="/"</script>'''
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Invalid name!'
            return '''<script>alert("Invalid name!");window.location="/"</script>'''
        elif not re.match(r'[A-Za-z0-9]+', address):
            msg = 'Invalid address!'
            return '''<script>alert("Invalid address!");window.location="/"</script>'''
        elif not re.match(r'[0-9]+', phone_no):
            msg = 'Invalid phone number!'
            return '''<script>alert("Invalid Phone number!");window.location="/"</script>'''
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Invalid password!'
            return '''<script>alert("Invalid password!");window.location="/"</script>'''
        elif not username or not password:
            msg = 'Please fill out the form!'
            return '''<script>alert("Please fill out the form!");window.location="/"</script>'''
        elif not username and not name and not address and not phone_no and not password:
            return '''<script>alert("Please fill out the form!");window.location="/"</script>'''
        else:
            cursor.execute('INSERT INTO user_reg VALUES (%s, %s, %s, %s, %s,%s)', (username, name, address, phone_no, password,options))
            conn.commit()
            return '''<script>alert("Registration successfull");window.location="/"</script>'''
            # if request.method == 'POST':        # elif to if 
            #     msg = 'Please fill out the form!'
    return render_template('registration.html', msg=msg)


# Admin

@app.route('/adminhome')
def adminhome():            #  == "ii":      removed
    return render_template('adminhome.html')
    # else:
    # return redirect(url_for('login'))


@app.route('/addOwner')
def addOwner():
    return render_template('addowner.html')


@app.route('/addclient',methods=['GET','POST'])
def addclient():
    o_id = request.form['ownerid']
    name = request.form['ownername']
    address = request.form['owneradd']
    phone_no = request.form['ownerph']
    password = request.form['ownerpass']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('INSERT INTO owner_reg VALUES (%s, %s, %s, %s, %s)', (o_id, name, address, phone_no, password))
    conn.commit()
    msg = 'add client successfully!'
    return render_template('addowner.html', msg=msg)

    return redirect(url_for('login'))


@app.route('/viewclient')
def viewclient():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM owner_reg')
    client = cursor.fetchall()
    print(len(client))
    print(client)
    return render_template('viewowner.html',data=client,len = len(client))

@app.route('/upclient')
def upclient():
    return render_template('updateowner.html')


@app.route('/updateclient', methods=['GET','POST'])
def updateclient():
    cursor = mysql.connect().cursor()
    cur = mysql.connect().cursor(pymysql.cursors.DictCursor)
    
    ownerid = request.form['ownerid']
    ownername = request.form['ownername']
    phonenumber = request.form['phone']
    address = request.form['address']
    password = request.form['pass']
    cur.execute(
        "UPDATE owner_reg SET o_id = %s, name = %s, address = %s, phone_no = %s, password = %s WHERE o_id = %s ",
        (ownerid, ownername, address,phonenumber, password,ownerid))
    mysql.connect().commit()
    cur.close()
    msg = 'client successfully Updated'
    return render_template("updateowner.html",data=msg)


@app.route('/viewuser')
def viewuser():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_reg WHERE id = %s', [session['id']])
    user_reg = cursor.fetchone()


def updateuser():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        txtuserid = request.form['txtuserid']
        txtname = request.form['txtname']
        txtaddress = request.form['txtaddress']
        txtphonenumber = request.form['txtphonenumber']
        txtpassword = request.form['txtpassword']
        print(string)
        cur.execute("UPDATE user_reg SET name = %s, department = %s, phone = %s WHERE id = %s ",
                    [txtuserid, txtname, txtaddress, txtphonenumber, txtpassword, string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record successfully Updated'
    return (msg)
    return render_template('view user.html')

@app.route('/viewcategories')
def viewcategoies():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM category')
    categories = cursor.fetchall()
    print(categories)
    return render_template('viewcategory.html',data=categories)


    return redirect(url_for('login'))


@app.route('/viewproduct')
def viewproduct():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE p_id = %s', [session['id']])
    products = cursor.fetchone()


def viewrating():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM rating WHERE r_id = %s', [session['id']])
    rating = cursor.fetchone()
    return render_template('view product.html')


    return redirect(url_for('login'))


# Client

@app.route('/clienthome')
def clienthome(): #== "ii":
    return render_template('ownerhome.html')
# else:
#     return redirect(url_for('login'))

@app.route('/updateproperty')
def updateproperty():
    return render_template('updateproperty.html')

@app.route('/updateproTODB',methods=['GET','POST'])
def updateproTODB():
    ownerd = request.form['ownerd']
    Loc = request.form['Loc']
    plot = request.form['plot']
    prodes = request.form['prodes']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("UPDATE property SET Loc = %s, plot = %s, prodes = %s  where ownerd = %s",
                    (Loc, plot, prodes,ownerd))
    conn.commit()
    msg = "updated successfully"
    return render_template('updateproperty.html',data=msg)
    



@app.route('/addproducts')
def addproducts():
    return render_template('addproperty.html')

@app.route('/addproduct')
def addproduct():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('INSERT INTO products VALUES (NULL, %s, %s, %s, %s, %s)', (productid, name, modelnumber, price, image, productdetails))
    conn.commit()
    msg = 'add product sucessfully!'
    return render_template('addproducts.html', msg=msg)
    return redirect(url_for('login'))


# @app.route('/viewrating')         #/viewproduct/updateproduct/
# def viewproduct():
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute('SELECT * FROM products WHERE p_id = %s', [session['id']])
#     products = cursor.fetchone()


def viewrating():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM rating WHERE r_id = %s', [session['id']])
    rating = cursor.fetchone()


def updateproduct():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        txtname = request.form['txtname']
        txtmodelnumber = request.form['txtaddress']
        txtprice = request.form['txtphonenumber']
        image = request.form['image']
        txtproductdetails = request.form['txtproductdetails']
        print(string)
        cur.execute("UPDATE user_reg SET name = %s, model_no = %s, price = %s, p_details = %s WHERE id = %s ",
                    [txtname, txtmodelnumber, txtprice, txtproductdetails, image, string])
        mysql.connection.commit()
        cur.close()
        msg = 'product successfully Updated'
    return (msg)
    return render_template('view product.html')


    return redirect(url_for('login'))


@app.route('/Addcat')
def Addcat():
    return render_template('addcategory.html')

@app.route('/addcategories',methods=['GET','POST'])
def addcategories():
    import random
    paying_guest_details = random.randint(0,22)
    rent_house_details = request.form['pay']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('INSERT INTO category VALUES (%s, %s)', (paying_guest_details, rent_house_details))
    conn.commit()
    msg = 'add categories successfully!'
    #return '''<script>alert("updated successfully!");window.location="/"</script>'''
    #return redirect(url_for('login'))
    return render_template('addcategory.html',data=msg)

@app.route('/viewcategories')
def viewcategories():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM category')
    categories = cursor.fetchone()
    print(categories)

@app.route('/updateCatPage')
def updateCatPage():
    return render_template('updatecategory.html')

@app.route('/updatecategories')
def updatecategories():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        txtcategoryid = request.form['txtcategoryid']
        txtcategoryname = request.form['txtcategoryname']
        print(string)
        cur.execute("UPDATE categories SET cat_id = %s, cat_name WHERE cat_id = %s ", [txtcategoryid, txtcategoryname])
        mysql.connection.commit()
        cur.close()
        msg = 'categories successfully Updated'
    return(msg)


# @app.route('/viewuser')
# def viewuser():
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute('SELECT * FROM user_reg WHERE id = %s', [session['id']])
#     user_reg = cursor.fetchone()
#     return render_template('view user.html')


#     return redirect(url_for('login'))


# User

# @app.route('/userhome')
# def userhome(): #=="ii"
#     return render_template('/home.html')
# # else:
# #     return redirect(url_for('login'))


# @app.route('/viewproduct')
# def viewproduct():
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute('SELECT * FROM products WHERE p_id = %s', [session['id']])
#     products = cursor.fetchone()


def viewrating():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM rating WHERE r_id = %s', [session['id']])
    rating = cursor.fetchone()


def addrating():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('INSERT INTO rating VALUES (NULL, %s, %s)', (rateid, rate, description))
    conn.commit()


def viewcategories():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM categories WHERE cat_id = %s', [session['id']])
    categories = cursor.fetchone()
    return render_template('view product.html')


    return redirect(url_for('login'))


@app.route("/viewproperty")
def viewproperty():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM property')
    property = cursor.fetchall()
    print(property)
    return render_template('viewproperty.html',data=property)


@app.route('/editprofile')
def editprofile():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_reg WHERE user_id = %s', [session['id']])
    user_reg = cursor.fetchone()
    return render_template('editprofile.html',data = user_reg)


    return redirect(url_for('login'))

@app.route('/addPropertyToDB',methods=['GET','POST'])
def addPropertyToDB():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    ownerd = request.form['ownerd']
    Loc = request.form['loc']
    plot = request.form['plot']
    prodes = request.form['prodes']
    cursor.execute("INSERT INTO property values(%s,%s,%s,%s)",(ownerd, Loc, plot, prodes))
    conn.commit()
    msg = "updated successfully"
    return render_template("addproperty.html",data=msg)

@app.route('/viewPayment')
def viewPayment():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from payment")
    result = cursor.fetchall()
    return render_template('viewpayment.html',data=result)

@app.route('/addpayment')
def addpayment():
    return render_template('addpayment.html')

@app.route("/processpayment",methods=['GET','POST'])
def processpayment():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    payment_id = request.form['payid']
    name = request.form['payname']
    amount = request.form['payamount']
    cursor.execute("INSERT INTO payment values(%s,%s,%s)",(payment_id, name, amount))
    conn.commit()
    msg = "payment successfull"
    return render_template("addpayment.html",data=msg)


@app.route('/addcomplaint')
def addcomplain():
    return render_template('addcomplaint.html')

@app.route('/processcomplaint',methods=['POST'])
def processcomplaint():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    name = request.form['name']
    description = request.form['desc']
    cursor.execute("INSERT INTO complaint values(%s,%s)",(name, description))
    conn.commit()
    msg = "complaint added!"
    return render_template('addcomplaint.html',data=msg)
@app.route('/viewcomplaint')
def viewcomplaint():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from complaint')
    result = cursor.fetchall()
    print(result)
    return render_template('viewcomplaint.html',data = result)

@app.route('/updatecomplaint')
def updatecomplaint():
    return render_template("updatecomplaint.html")

@app.route('/updateComplaintTODB', methods = ['GET','POST'])
def updateComplaintTODB():
    name = request.form['name']
    description = request.form['desc']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('UPDATE complaint SET name = %s, description = %s where name = %s',(name,description,name))
    conn.commit()
    msg = 'complaint updated!'
    return render_template("updatecomplaint.html", data = msg)
@app.route('/saveprofile', methods=['POST'])
def saveprofile():
    name = request.form['name']
    address = request.form['add']
    phone_no = request.form['phno']
    password = request.form['pass']
    conn= mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('UPDATE user_reg SET name = %s, address = %s ,phone_no = %s ,password = %s where user_id = %s',(name,address,phone_no, password, session['id']))
    conn.commit()
    profile = '''<script>alert("profile edited!");window.location="/"</script>'''
    return render_template('user_home.html', profileedit = profile)


@app.route("/viewprofile")
def viewprofile():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from user_reg where user_id = %s',(session['id']))
    result = cursor.fetchone()
    print(result)
    return render_template('viewprofile.html',data = result)

@app.route('/viewcustomer')
def viewcustomer():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from user_reg where options = 'user'")
    result = cursor.fetchall()
    return render_template("viewcustomer.html",data=result)

if __name__ == '__main__':
    app.run(debug=True)

