from flask import Flask, render_template, request, flash, redirect, url_for
import random
import string
import pandas as pd
import time
from credentials import conn

app = Flask(__name__)
app.secret_key = '(}v:}RbT}ygEz;i_38][q6gX_23}42f$viYC^#&6J7Fbk8AlK5Ez@uQBd#SGv5w7Hr$7#w$YM%pbC$W43P'

cur = conn.cursor()

cur.execute('CREATE DATABASE if not exists PasswordDatabase')
cur.execute('USE PasswordDatabase')

cur.execute('CREATE TABLE if not exists Password_Manager(id INT AUTO_INCREMENT PRIMARY KEY , username VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, site VARCHAR(30) NOT NULL)')

elements = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 \"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"


@app.route('/')
def main():
    return render_template('home.html')


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get the values of the domain, username, and password from the form
        domain = request.form["domain"]
        username = request.form["username"]
        password = request.form["password"]

        # To check if the service already exists in the database
        check = "SELECT * FROM Password_Manager WHERE site=%s AND username=%s"
        cur.execute(check, (domain, username))
        result = cur.fetchone()

        if result:
            flash('Service with same username already exists in the database')
            return redirect(url_for('add'))

        # Code to add the new password to the password manager database
        tup = (username, password, domain)
        code = "INSERT INTO Password_Manager (username, password, site) VALUES (%s,%s,%s)"
        cur.execute(code, tup)
        conn.commit()

        return redirect(url_for('add'))

    if request.method == "GET":
        return render_template("add.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    service = None

    if request.method == 'POST':
        service = request.form['service']
        cur.execute(
            "SELECT username, password FROM Password_Manager WHERE site=%s", (service,))
        results = cur.fetchall()

    return render_template('search.html', results=results, service=service)


@ app.route('/display_all')
def display_all():
    cur.execute("SELECT site, username, password FROM Password_Manager")
    results = cur.fetchall()
    return render_template('display_all.html', results=results)


@app.route('/delete_selected/<string:service>/<string:username>', methods=['POST'])
def delete_selected(service, username):
    cur.execute(
        "DELETE FROM Password_Manager WHERE site=%s and username=%s", (service, username))
    conn.commit()
    return redirect(url_for('display_all'))


if __name__ == '__main__':
    app.run(debug=True)
