import asyncio
import os
from asyncio import sleep

from flask import Flask, request, render_template, json, jsonify, url_for, redirect, session, flash
from flask_cors import CORS, cross_origin
from tg_bot.models.database_model import Database

app = Flask(__name__)
app.secret_key = 'password'
db = Database()
CORS(app)

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # getting input with name = login in HTML form
        login = request.form.get("login")
        # getting input with name = password in HTML form
        password = request.form.get("password")
        if login != 'admin' or password != 'password':
            error = 'Спробуйте знову, неправильний логін або пароль'
        else:
            return redirect(url_for('order'))
    return render_template("login.html", error=error)


@app.route('/order', methods=['POST', 'GET'])
def order():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
    try:
        return render_template('order.html')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    try:
        orders = db.select_all_orders()
        return orders
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"


# @app.route('/postmethod', methods=['POST'])
# def get_post_js_data():
#     jsdata = request.form['javascript_data']
#     print(str(jsdata))


@app.route('/home/<name>')
def main(name):
    if name == '/':
        return redirect(url_for('login'))
    if name == 'order':
        return redirect(url_for('order'))
    # if name == 'student':
    #     return redirect(url_for('student'))


if __name__ == "__main__":
    app.run(debug=True)

