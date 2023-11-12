from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(100))
  phone_number = db.Column(db.String(15))


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  price = db.Column(db.Float, nullable=False)


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False)
  product_id = db.Column(db.Integer, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  total_price = db.Column(db.Float, nullable=False)
  timestamp = db.Column(db.TIMESTAMP,
                        server_default=db.func.current_timestamp())
  user = db.relationship('User', backref='orders')
  product = db.relationship('Product', backref='orders')


class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(100))
  phone_number = db.Column(db.String(15))


class Payment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  payment_method = db.Column(db.String(50))
  payment_status = db.Column(db.String(50))
  timestamp = db.Column(db.TIMESTAMP,
                        server_default=db.func.current_timestamp())
  order = db.relationship('Order', backref='payments')


class Inventory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  product_id = db.Column(db.Integer, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  product = db.relationship('Product', backref='inventory')


class Sale(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, nullable=False)
  total_revenue = db.Column(db.Float, nullable=False)
  timestamp = db.Column(db.TIMESTAMP,
                        server_default=db.func.current_timestamp())
  order = db.relationship('Order', backref='sales')


class Deliveryman(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(100))
  phone_number = db.Column(db.String(15))


class Delivery(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, nullable=False)
  deliveryman_id = db.Column(db.Integer)
  delivery_status = db.Column(db.String(50))
  delivery_address = db.Column(db.String(255))
  delivery_timestamp = db.Column(db.TIMESTAMP)
  order = db.relationship('Order', backref='deliveries')
  deliveryman = db.relationship('Deliveryman', backref='deliveries')


@app.route('/')
def index():
  return 'Hello from Flask!'


app.run(host='0.0.0.0', port=81)
