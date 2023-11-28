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
        elif data['data'] == 'DELETED':
            try:
                db.create_table_old_orders()
                print('try to add order to old datatable')
                db.add_old_order(
                    order_id=data['orderID'],
                    name=data['userID'],
                    order_name='order# ' + data['orderID'],
                    smoke_strength_choice=data['strength'],
                    taste_choice=data['flavour'],
                    second_taste_choice=data['flavour1'],
                    third_taste_choice=data['flavour2'],
                    confirmed=True,
                    deleted=True
                )
                print('order was add to old datatable')
                db.delete_order(data['orderID'], 'orders_table')
                print('Order was deleted')
            except Exception as e:
                print(e, "exception")
            return 'ok'
    return 'ok'


@app.route('/old_order', methods=['GET', 'POST'])
def old_order():
    try:
        return render_template('old_order.html')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    try:
        orders = db.select_all_orders('orders_table')
        return orders
    except Exception as e:
        # e holds description of the error
        "<p>The error:<br>" + str(e) + "</p>"


@app.route('/api/get_old_orders', methods=['GET'])
def get_old_orders():
    try:
        orders = db.select_all_orders('create_table_old_orders')
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

