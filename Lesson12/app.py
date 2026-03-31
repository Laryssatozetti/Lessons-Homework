from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'secret'

DATA_FILE = 'history.txt'

# In-memory state
balance = 0.0
stock = {}


def save_history(line):
    try:
        with open(DATA_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception as e:
        print('Error writing to file:', e)


def load_history():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print('Error reading file:', e)
        return []


@app.route('/')
def index():
    total_stock = sum(stock.values())
    return render_template('index.html', balance=balance, stock=total_stock)


@app.route('/purchase', methods=['POST'])
def purchase():
    global balance, stock
    try:
        product = request.form['product']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        if price <= 0 or quantity <= 0:
            raise ValueError

        total_cost = price * quantity
        balance -= total_cost
        stock[product] = stock.get(product, 0) + quantity

        save_history(f"PURCHASE,{product},{quantity},{price}")

    except Exception:
        flash('Invalid purchase data')

    return redirect(url_for('index'))


@app.route('/sale', methods=['POST'])
def sale():
    global balance, stock
    try:
        product = request.form['product']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        if product not in stock or stock[product] < quantity:
            raise ValueError('Not enough stock')

        if price <= 0 or quantity <= 0:
            raise ValueError

        total_income = price * quantity
        balance += total_income
        stock[product] -= quantity

        save_history(f"SALE,{product},{quantity},{price}")

    except Exception:
        flash('Invalid sale data or insufficient stock')

    return redirect(url_for('index'))


@app.route('/balance', methods=['POST'])
def change_balance():
    global balance
    try:
        operation = request.form['operation']
        amount = float(request.form['amount'])

        if amount <= 0:
            raise ValueError

        if operation == 'add':
            balance += amount
        elif operation == 'subtract':
            balance -= amount
        else:
            raise ValueError

        save_history(f"BALANCE,{operation},{amount}")

    except Exception:
        flash('Invalid balance operation')

    return redirect(url_for('index'))


@app.route('/history/')
@app.route('/history/<int:line_from>/<int:line_to>/')
def history(line_from=None, line_to=None):
    history_data = load_history()
    if line_from is not None and line_to is not None:
        history_data = history_data[line_from:line_to]
    return render_template('history.html', history=history_data)


if __name__ == '__main__':
    app.run(debug=True)