import js2py
from flask import Flask, request, render_template, json, jsonify, url_for, redirect, session, flash
from flask_cors import CORS, cross_origin
from bot_main import db
from get_data import get_data_js_string
from tg_bot.handlers.bot_send_custom_message_to_user import send_message_to_user

app = Flask(__name__)
app.secret_key = 'password'
CORS(app)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # getting input with name = login in HTML form
        log_in = request.form.get("login")
        # getting input with name = password in HTML form
        password = request.form.get("password")
        if log_in != 'admin' or password != 'password':
            error = 'Спробуйте знову, неправильний логін або пароль'
        else:
            return redirect(url_for('order'))
    return render_template("login.html", error=error)


@app.route('/order', methods=['GET'])
def order():
    try:
        return render_template('order.html')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/order', methods=['POST'])
async def get_data_from_buttons():
    if request.method != 'POST':
        return 'ok'
    elif request.method == 'POST':
        data = request.form.to_dict()
        if data['data'] == 'CONFIRMED':
            await send_message_to_user(data)
            return 'ok'
        else:
            return 'ok'
    return 'ok'


@app.route('/order-test', methods=['GET', 'POST'])
def build_orders():
    return render_template('order_test.html')


@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    try:
        orders = db.select_all_orders()
        return orders
    except Exception as e:
        # e holds description of the error
        "<p>The error:<br>" + str(e) + "</p>"


# @app.route('/postmethod', methods=['POST'])
# def get_post_js_data():
#     jsdata = request.form['javascript_data']
#     print(str(jsdata))


if __name__ == "__main__":
    app.run(debug=True)

