from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.secret_key = "caircocoders-ednalan"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ' houserent'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/updatecomplaint/')
def updatecomplaint():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM complaints ORDER BY id")
    employee = cur.fetchall()
    return render_template('updatecomplaint.html', employee=employee)


@app.route("/ajax_add", methods=["POST", "GET"])
def ajax_add():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        txtname = request.form['txtname']
        txtdescription = request.form['txtdescription']
        image = request.form['image']
        print(txtname)
        if txtname == '':
            msg = 'Please Input name'
        elif txtdescription == '':
            msg = 'Please Input Description'
        elif image == '':
            msg = 'Please Input Image'
        else:
            cur.execute("INSERT INTO complaints (name,description,image) VALUES (%s,%s,%s)",
                        [txtname, txtdescription, image])
            mysql.connection.commit()
            cur.close()
            msg = 'New record created successfully'
    return jsonify(msg)


@app.route("/ajax_update", methods=["POST", "GET"])
def ajax_update():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        txtname = request.form['txtname']
        txtdescription = request.form['txtdescription']
        image = request.form['image']
        print(string)
        cur.execute("UPDATE complaints SET name = %s, description = %s, image = %s WHERE id = %s ",
                    [txtname, txtdescription, image, string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record successfully Updated'
    return jsonify(msg)


@app.route("/ajax_delete", methods=["POST", "GET"])
def ajax_delete():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('DELETE FROM complaints WHERE id = {0}'.format(getid))
        mysql.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


if __name__ == "__main__":
    app.run(debug=True)