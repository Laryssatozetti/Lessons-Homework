from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# =========================
# MODELS
# =========================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# Inicializa DB
# =========================
with app.app_context():
    db.create_all()
    # Cria uma linha de saldo se não existir
    if not Balance.query.first():
        db.session.add(Balance(amount=0.0))
        db.session.commit()

# =========================
# ROTAS
# =========================
@app.route('/')
def index():
    balance_obj = Balance.query.first()
    total_stock = sum([p.quantity for p in Product.query.all()])
    return render_template('index.html', balance=balance_obj.amount, stock=total_stock)

# -------- PURCHASE --------
@app.route('/purchase', methods=['POST'])
def purchase():
    try:
        product_name = request.form['product']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        if price <= 0 or quantity <= 0:
            raise ValueError

        # Atualiza estoque
        product = Product.query.filter_by(name=product_name).first()
        if not product:
            product = Product(name=product_name, quantity=quantity)
            db.session.add(product)
        else:
            product.quantity += quantity

        # Atualiza saldo
        balance_obj = Balance.query.first()
        balance_obj.amount -= price * quantity

        # Salva transação
        transaction = Transaction(type='purchase', product_name=product_name, quantity=quantity, price=price)
        db.session.add(transaction)

        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Invalid purchase data')
    return redirect(url_for('index'))

# -------- SALE --------
@app.route('/sale', methods=['POST'])
def sale():
    try:
        product_name = request.form['product']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        product = Product.query.filter_by(name=product_name).first()
        if not product or product.quantity < quantity or price <= 0 or quantity <= 0:
            raise ValueError

        # Atualiza estoque
        product.quantity -= quantity

        # Atualiza saldo
        balance_obj = Balance.query.first()
        balance_obj.amount += price * quantity

        # Salva transação
        transaction = Transaction(type='sale', product_name=product_name, quantity=quantity, price=price)
        db.session.add(transaction)

        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Invalid sale data or insufficient stock')
    return redirect(url_for('index'))

# -------- BALANCE --------
@app.route('/balance', methods=['POST'])
def change_balance():
    try:
        operation = request.form['operation']
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError

        balance_obj = Balance.query.first()
        if operation == 'add':
            balance_obj.amount += amount
        elif operation == 'subtract':
            balance_obj.amount -= amount
        else:
            raise ValueError

        # Salva transação
        transaction = Transaction(type='balance', quantity=None, price=amount, product_name=None)
        db.session.add(transaction)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Invalid balance operation')
    return redirect(url_for('index'))

# -------- HISTORY --------
@app.route('/history/')
@app.route('/history/<int:line_from>/<int:line_to>/')
def history(line_from=None, line_to=None):
    try:
        query = Transaction.query.order_by(Transaction.id).all()
        if line_from is not None and line_to is not None:
            query = query[line_from:line_to]
    except Exception:
        flash('Error retrieving history')
        query = []
    return render_template('history.html', history=query)

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=5001)