from flask import Flask, request, jsonify, render_template
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

    def __init__(self, username, password, first_name=None, last_name=None, email=None, phone_number=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    def __init__(self, user_id, product_id, quantity, total_price):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))

    def __init__(self, first_name, last_name, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    order = db.relationship('Order', backref='payments')

    def __init__(self, order_id, amount, payment_method, payment_status):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='inventory')

    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    order = db.relationship('Order', backref='sales')

    def __init__(self, order_id, total_revenue):
        self.order_id = order_id
        self.total_revenue = total_revenue


class Deliveryman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))

    def __init__(self, first_name, last_name, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    deliveryman_id = db.Column(db.Integer)
    delivery_status = db.Column(db.String(50))
    delivery_address = db.Column(db.String(255))
    delivery_timestamp = db.Column(db.TIMESTAMP)
    order = db.relationship('Order', backref='deliveries')
    deliveryman = db.relationship('Deliveryman', backref='deliveries')

    def __init__(self, order_id, deliveryman_id, delivery_status, delivery_address, delivery_timestamp):
        self.order_id = order_id
        self.deliveryman_id = deliveryman_id
        self.delivery_status = delivery_status
        self.delivery_address = delivery_address
        self.delivery_timestamp = delivery_timestamp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/users', methods=['GET', 'POST'])
def api_manage_users():
    if request.method == 'GET':
        users = User.query.all()
        user_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users]
        return jsonify(user_list)

    elif request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'],
                        password=data['password'],
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        email=data.get('email'),
                        phone_number=data.get('phone_number'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201


@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

    elif request.method == 'PUT':
        data = request.json
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})


@app.route('/api/products', methods=['GET', 'POST'])
def api_manage_products():
    if request.method == 'GET':
        products = Product.query.all()
        product_list = [{
            'id': product.id,
            'name': product.name,
            'price': product.price
        } for product in products]
        return jsonify(product_list)

    elif request.method == 'POST':
        data = request.json
        new_product = Product(name=data['name'], price=data['price'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201


@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'GET':
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price
        })

    elif request.method == 'PUT':
        data = request.json
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})


@app.route('/api/orders', methods=['GET', 'POST'])
def api_manage_orders():
    if request.method == 'GET':
        orders = Order.query.all()
        order_list = [{
            'id': order.id,
            'user_id': order.user_id,
            'product_id': order.product_id,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'timestamp': order.timestamp
        } for order in orders]
        return jsonify(order_list)

    elif request.method == 'POST':
        data = request.json
        new_order = Order(user_id=data['user_id'],
                          product_id=data['product_id'],
                          quantity=data['quantity'],
                          total_price=data['total_price'])
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201


@app.route('/api/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'GET':
        return jsonify({
            'id': order.id,
            'user_id': order.user_id,
            'product_id': order.product_id,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'timestamp': order.timestamp
        })

    elif request.method == 'PUT':
        data = request.json
        order.user_id = data.get('user_id', order.user_id)
        order.product_id = data.get('product_id', order.product_id)
        order.quantity = data.get('quantity', order.quantity)
        order.total_price = data.get('total_price', order.total_price)
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'})


@app.route('/api/customers', methods=['GET', 'POST'])
def api_manage_customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        customer_list = [{
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone_number': customer.phone_number
        } for customer in customers]
        return jsonify(customer_list)

    elif request.method == 'POST':
        data = request.json
        new_customer = Customer(first_name=data.get('first_name'),
                                last_name=data.get('last_name'),
                                email=data.get('email'),
                                phone_number=data.get('phone_number'))
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully'}), 201


@app.route('/api/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'GET':
        return jsonify({
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone_number': customer.phone_number
        })

    elif request.method == 'PUT':
        data = request.json
        customer.first_name = data.get('first_name', customer.first_name)
        customer.last_name = data.get('last_name', customer.last_name)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})


@app.route('/api/payments', methods=['GET', 'POST'])
def api_manage_payments():
    if request.method == 'GET':
        payments = Payment.query.all()
        payment_list = [{
            'id': payment.id,
            'order_id': payment.order_id,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'payment_status': payment.payment_status,
            'timestamp': payment.timestamp
        } for payment in payments]
        return jsonify(payment_list)

    elif request.method == 'POST':
        data = request.json
        new_payment = Payment(order_id=data['order_id'],
                              amount=data['amount'],
                              payment_method=data['payment_method'],
                              payment_status=data['payment_status'])
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({'message': 'Payment created successfully'}), 201


@app.route('/api/payments/<int:payment_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)

    if request.method == 'GET':
        return jsonify({
            'id': payment.id,
            'order_id': payment.order_id,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'payment_status': payment.payment_status,
            'timestamp': payment.timestamp
        })

    elif request.method == 'PUT':
        data = request.json
        payment.order_id = data.get('order_id', payment.order_id)
        payment.amount = data.get('amount', payment.amount)
        payment.payment_method = data.get('payment_method', payment.payment_method)
        payment.payment_status = data.get('payment_status', payment.payment_status)
        db.session.commit()
        return jsonify({'message': 'Payment updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'})


@app.route('/api/inventory', methods=['GET', 'POST'])
def api_manage_inventory():
    if request.method == 'GET':
        inventory = Inventory.query.all()
        inventory_list = [{
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity
        } for item in inventory]
        return jsonify(inventory_list)

    elif request.method == 'POST':
        data = request.json
        new_inventory = Inventory(product_id=data['product_id'],
                                  quantity=data['quantity'])
        db.session.add(new_inventory)
        db.session.commit()
        return jsonify({'message': 'Inventory item created successfully'}), 201


@app.route('/api/sales', methods=['GET', 'POST'])
def api_manage_sales():
    if request.method == 'GET':
        sales = Sale.query.all()
        sale_list = [{
            'id': sale.id,
            'order_id': sale.order_id,
            'total_revenue': sale.total_revenue,
            'timestamp': sale.timestamp
        } for sale in sales]
        return jsonify(sale_list)

    elif request.method == 'POST':
        data = request.json
        new_sale = Sale(order_id=data['order_id'],
                        total_revenue=data['total_revenue'])
        db.session.add(new_sale)
        db.session.commit()
        return jsonify({'message': 'Sale created successfully'}), 201


@app.route('/api/sales/<int:sale_id>', methods=['GET', 'PUT', 'DELETE'])
def api_manage_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    if request.method == 'GET':
        return jsonify({
            'id': sale.id,
            'order_id': sale.order_id,
            'total_revenue': sale.total_revenue,
            'timestamp': sale.timestamp
        })

    elif request.method == 'PUT':
        data = request.json
        sale.order_id = data.get('order_id', sale.order_id)
        sale.total_revenue = data.get('total_revenue', sale.total_revenue)
        db.session.commit()
        return jsonify({'message': 'Sale updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(sale)
        db.session.commit()
        return jsonify({'message': 'Sale deleted successfully'})


@app.route('/api/deliverymen', methods=['GET', 'POST'])
def api_manage_deliverymen():
    if request.method == 'GET':
        deliverymen = Deliveryman.query.all()
        deliverymen_list = [{
            'id': deliveryman.id,
            'first_name': deliveryman.first_name,
            'last_name': deliveryman.last_name,
            'email': deliveryman.email,
            'phone_number': deliveryman.phone_number
        } for deliveryman in deliverymen]
        return jsonify(deliverymen_list)

    elif request.method == 'POST':
        data = request.json
        new_deliveryman = Deliveryman(first_name=data.get('first_name'),
                                      last_name=data.get('last_name'),
                                      email=data.get('email'),
                                      phone_number=data.get('phone_number'))
        db.session.add(new_deliveryman)
        db.session.commit()
        return jsonify({'message': 'Deliveryman created successfully'}), 201


@app.route('/api/deliverymen/<int:deliveryman_id>',
           methods=['GET', 'PUT', 'DELETE'])
def api_manage_deliveryman(deliveryman_id):
    deliveryman = Deliveryman.query.get_or_404(deliveryman_id)

    if request.method == 'GET':
        return jsonify({
            'id': deliveryman.id,
            'first_name': deliveryman.first_name,
            'last_name': deliveryman.last_name,
            'email': deliveryman.email,
            'phone_number': deliveryman.phone_number
        })

    elif request.method == 'PUT':
        data = request.json
        deliveryman.first_name = data.get('first_name', deliveryman.first_name)
        deliveryman.last_name = data.get('last_name', deliveryman.last_name)
        deliveryman.email = data.get('email', deliveryman.email)
        deliveryman.phone_number = data.get('phone_number',
                                            deliveryman.phone_number)
        db.session.commit()
        return jsonify({'message': 'Deliveryman updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(deliveryman)
        db.session.commit()
        return jsonify({'message': 'Deliveryman deleted successfully'})


@app.route('/api/deliveries', methods=['GET', 'POST'])
def api_manage_deliveries():
    if request.method == 'GET':
        deliveries = Delivery.query.all()
        delivery_list = [{
            'id': delivery.id,
            'order_id': delivery.order_id,
            'deliveryman_id': delivery.deliveryman_id,
            'delivery_status': delivery.delivery_status,
            'delivery_address': delivery.delivery_address,
            'delivery_timestamp': delivery.delivery_timestamp
        } for delivery in deliveries]
        return jsonify(delivery_list)

    elif request.method == 'POST':
        data = request.json
        new_delivery = Delivery(order_id=data['order_id'],
                                deliveryman_id=data['deliveryman_id'],
                                delivery_status=data['delivery_status'],
                                delivery_address=data['delivery_address'],
                                delivery_timestamp=data['delivery_timestamp'])
        db.session.add(new_delivery)
        db.session.commit()
        return jsonify({'message': 'Delivery created successfully'}), 201


@app.route('/api/deliveries/<int:delivery_id>',
           methods=['GET', 'PUT', 'DELETE'])
def api_manage_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)

    if request.method == 'GET':
        return jsonify({
            'id': delivery.id,
            'order_id': delivery.order_id,
            'deliveryman_id': delivery.deliveryman_id,
            'delivery_status': delivery.delivery_status,
            'delivery_address': delivery.delivery_address,
            'delivery_timestamp': delivery.delivery_timestamp
        })

    elif request.method == 'PUT':
        data = request.json
        delivery.order_id = data.get('order_id', delivery.order_id)
        delivery.deliveryman_id = data.get('deliveryman_id',
                                           delivery.deliveryman_id)
        delivery.delivery_status = data.get('delivery_status',
                                            delivery.delivery_status)
        delivery.delivery_address = data.get('delivery_address',
                                             delivery.delivery_address)
        delivery.delivery_timestamp = data.get('delivery_timestamp',
                                               delivery.delivery_timestamp)
        db.session.commit()
        return jsonify({'message': 'Delivery updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(delivery)
        db.session.commit()
        return jsonify({'message': 'Delivery deleted successfully'})


if __name__ == '__main__':
  with app.app_context():
      db.create_all()
  app.run(debug=True, port=5000)
