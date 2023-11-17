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


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # getting input with name = login in HTML form
        login = request.form.get("login")
        # getting input with name = password in HTML form
        password = request.form.get("password")
        if login != 'admin' or password != 'password':
            error = 'Спробуйте знову, неправильний логін або пароль'
        else:
            return main_page()
    return render_template("index.html", error=error)


@app.route('/order',  methods=["GET", "POST"])
def main_page():
    try:
        orders = db.select_all_orders()
        # print("Order page was refreshed")
        return render_template('order.html', orders=orders)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    try:
        orders = db.select_all_orders()
        print("Order page was refreshed")
        data = jsonify(orders)
        # print(orders)
        # print(jsonify(orders))
        return orders
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"


if __name__ == "__main__":
    app.run(debug=True)

