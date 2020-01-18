import atexit
import os
import sqlite3
import os.path

# ------------------------------------DTO-------------------------------
# Data Transfer Objects
class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


# ------------------------------------DAO-------------------------------
# Data Access Objects
class _Activities:
    def __init__(self, dbcon):
        self._dbcon = dbcon

    def insert(self, activity):
        self._conn.execute("""
               INSERT INTO Activities (product_id, quantity, activator_id,date) VALUES (?,?,?,?)
           """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])


class _Coffee_stands:
    def __init__(self, dbcon):
        self._dbcon = dbcon

    def insert(self, coffee_stand):
        self._dbcon.execute("""
               INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?,?,?)
           """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])


class _Employees:
    def __init__(self, dbcon):
        self._dbcon = dbcon

    def insert(self, employee):
        self._dbcon.execute("""
               INSERT INTO Employees (id, name, salary,coffee_stand) VALUES (?,?,?,?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])


class _Suppliers:
    def __init__(self, dbcon):
        self._dbcon = dbcon

    def insert(self, supplier):
        self._dbcon.execute("""
               INSERT INTO Suppliers (id, name, contact_information) VALUES (?,?,?)
           """, [supplier.id, supplier.name, supplier.contact_information])


class _Products:
    def __init__(self, dbcon):
        self._dbcon = dbcon

    def insert(self, product):
        self._dbcon.execute("""
               INSERT INTO Products (id, description, price,quantity) VALUES (?,?,?,?)
           """, [product.id, product.description, product.price, product.quantity])

    def quantity_check(self, product_id):
        c = self._dbcon.cursor()
        c.execute("""
                SELECT quantity FROM Products WHERE id = ?
                """, [product_id])
        return c.fetchone()

    def update_quantity(self, product_id, new_quantity):
        c = self._dbcon.cursor()
        c.execute("""
                UPDATE Products SET quantity = ? WHERE id = ?
                """, [new_quantity, product_id])


# ------------------------------------Repository-------------------------------
# The Repository
class _Repository:
    def __init__(self):
        # Creation of a new database
        if os.path.isfile('moncafe.db'):
            os.remove('moncafe.db')  # Removing the old db
        BASE_DIR = os.path.dirname(os.path.abspath('./src'))
        db_path = os.path.join(BASE_DIR, "moncafe.db")
        self._dbcon = sqlite3.connect(db_path)
        self.activities = _Activities(self._dbcon)
        self.coffee_stands = _Coffee_stands(self._dbcon)
        self.employees = _Employees(self._dbcon)
        self.suppliers = _Suppliers(self._dbcon)
        self.products = _Products(self._dbcon)

    def _close(self):
        self._dbcon.commit()
        self._dbcon.close()

    def create_tables(self):
        self._dbcon.executescript("""
        CREATE TABLE Employees (
                           id INTEGER PRIMARY KEY, 
                           name TEXT NOT NULL, 
                           salary REAL NOT NULL, 
                           coffee_stand INTEGER REFERENCES Coffee_stands(id)
        );

        CREATE TABLE Suppliers(
                           id INTEGER PRIMARY KEY,
                           name TEXT NOT NULL,
                           contact_information TEXT
        );

        CREATE TABLE Products(
                           id INTEGER PRIMARY KEY,
                           description TEXT NOT NULL,
                           price REAL NOT NULL,
                           quantity INTEGER NOT NULL
        );
        
        CREATE TABLE Coffee_stands(
                           id INTEGER PRIMARY KEY,
                           location TEXT NOT NULL,
                           number_of_employees INTEGER
        );
        
        CREATE TABLE Activities(
                           product_id INTEGER INTEGER REFERENCES Product(id),
                           quantity INTEGER NOT NULL,
                           activator_id INTEGER NOT NULL,
                           date DATE NOT NULL
        );
    """)


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
