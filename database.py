import sqlite3


def create_tables(connection):
  cursor = connection.cursor()

  # Users table
  cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT
        )
    ''')

  # Products table
  cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    ''')

  # Orders table
  cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

  # Customers table
  cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT
        )
    ''')

  # Payments table
  cursor.execute('''
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            payment_method TEXT,
            payment_status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')

  # Inventory table
  cursor.execute('''
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

  # Sales table
  cursor.execute('''
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            total_revenue DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')

  # Deliverymen table
  cursor.execute('''
        CREATE TABLE deliverymen (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT
        )
    ''')

  # Deliveries table
  cursor.execute('''
        CREATE TABLE deliveries (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            deliveryman_id INTEGER,
            delivery_status TEXT,
            delivery_address TEXT,
            delivery_timestamp TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (deliveryman_id) REFERENCES deliverymen(id)
        )
    ''')

  connection.commit()


def main():
  # Connect to SQLite database (creates a new file if not exists)
  connection = sqlite3.connect('pos_database.db')

  # Create tables
  create_tables(connection)

  # Close the connection
  connection.close()


if __name__ == "__main__":
  main()
