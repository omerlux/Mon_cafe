import atexit
import inspect
import os
import sqlite3
import os.path


# ------------------------------------DTO-------------------------------
# Data Transfer Objects
# ----- Activity - DTO -----
class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        return str(self.product_id) + " " + str(self.quantity) + " " + str(self.activator_id) + " " + str(self.date)


# ----- Coffee_stand - DTO -----
class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        return str(self.id) + " " + self.location + " " + str(self.number_of_employees)


# ----- Employee - DTO -----
class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def __str__(self):
        return str(self.id) + " " + self.name + " " + str(self.salary) + " " + str(self.coffee_stand)


# ----- Supplier - DTO -----
class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        return str(self.id) + " " + self.name + " " + str(self.contact_information)


# ----- Product - DTO -----
class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return str(self.id) + " " + self.description + " " + str(self.price) + " " + str(self.quantity)


# ------------------------------------DAO-------------------------------
# Data Access Objects
# ----- Activities - DAO -----
class _Activities:
    def __init__(self, dbcon, dto_type):
        self._dbcon = dbcon
        self._dto_type = dto_type

    def insert(self, activity):
        self._dbcon.execute("""
               INSERT INTO Activities (product_id, quantity, activator_id,date) VALUES (?,?,?,?)
           """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def print(self):
        c = self._dbcon.cursor()
        allact = c.execute("""SELECT * FROM Activities ORDER BY Activities.date ASC""").fetchall()
        return [Activity(*row) for row in allact]


# ----- Coffee_stands - DAO -----
class _Coffee_stands:
    def __init__(self, dbcon, dto_type):
        self._dbcon = dbcon
        self._dto_type = dto_type

    def insert(self, coffee_stand):
        self._dbcon.execute("""
               INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?,?,?)
           """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def print(self):
        c = self._dbcon.cursor()
        allcs = c.execute("""SELECT * FROM Coffee_stands ORDER BY Coffee_stands.id ASC""").fetchall()
        return [Coffee_stand(*row) for row in allcs]


# ----- Employees - DAO -----
class _Employees:
    def __init__(self, dbcon, dto_type):
        self._dbcon = dbcon
        self._dto_type = dto_type

    def insert(self, employee):
        self._dbcon.execute("""
               INSERT INTO Employees (id, name, salary,coffee_stand) VALUES (?,?,?,?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def print(self):
        c = self._dbcon.cursor()
        allemp = c.execute("""SELECT * FROM Employees ORDER BY Employees.id ASC""").fetchall()
        return [Employee(*row) for row in allemp]


# ----- Suppliers - DAO -----
class _Suppliers:
    def __init__(self, dbcon, dto_type):
        self._dbcon = dbcon
        self._dto_type = dto_type

    def insert(self, supplier):
        self._dbcon.execute("""
               INSERT INTO Suppliers (id, name, contact_information) VALUES (?,?,?)
           """, [supplier.id, supplier.name, supplier.contact_information])

    def print(self):
        c = self._dbcon.cursor()
        allsupp = c.execute("""SELECT * FROM Suppliers ORDER BY Suppliers.id ASC""").fetchall()
        return [Supplier(*row) for row in allsupp]


# ----- Products - DAO -----
class _Products:
    def __init__(self, dbcon, dto_type):
        self._dbcon = dbcon
        self._dto_type = dto_type

    def insert(self, product):
        self._dbcon.execute("""
               INSERT INTO Products (id, description, price,quantity) VALUES (?,?,?,?)
           """, [product.id, product.description, product.price, product.quantity])

    def print(self):
        c = self._dbcon.cursor()
        allprod = c.execute("""SELECT * FROM Products ORDER BY Products.id ASC""").fetchall()
        return [Product(*row) for row in allprod]

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


# ----- Printing stuff - ORM -----
# for printing - creating a map of values for the specified dto
def orm(cursor, dto_type):
    # the following line retrieve the argument names of the constructor
    args = inspect.getfullargspec(dto_type.__init__).args

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


# ------------------------------------Repository-------------------------------
# The Repository
class _Repository:
    def __init__(self):
        # Creation of a new database
        BASE_DIR = os.path.dirname(os.path.abspath('./src'))
        db_path = os.path.join(BASE_DIR, "moncafe.db")
        self._dbcon = sqlite3.connect(db_path)
        self.activities = _Activities(self._dbcon, Activity)
        self.coffee_stands = _Coffee_stands(self._dbcon, Coffee_stand)
        self.employees = _Employees(self._dbcon, Employee)
        self.suppliers = _Suppliers(self._dbcon, Supplier)
        self.products = _Products(self._dbcon, Product)

    def _close(self):
        self._dbcon.commit()
        # self._dbcon.close()

    def _connect(self):
        self._dbcon = sqlite3.connect('moncafe.db')

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

    def get_extra_activities(self):
        c = self._dbcon.cursor()
        return c.execute("""SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name
                            FROM (Activities
                            INNER JOIN Products ON Activities.product_id=Products.id
                            LEFT OUTER JOIN Employees ON Activities.activator_id=Employees.id
                            LEFT OUTER JOIN Suppliers ON Activities.activator_id=Suppliers.id)
                            ORDER BY Activities.date ASC
                    """)

    def get_employees_report(self):
        c = self._dbcon.cursor()
        return c.execute("""SELECT Employees.name, Employees.salary, Coffee_stands.location, 
                            COALESCE (SUM( (Activities.quantity * Products.price)*(-1) ), 0)         
                            FROM (Employees
                            INNER JOIN Coffee_stands ON Employees.coffee_stand=Coffee_stands.id
                            LEFT OUTER JOIN Activities ON Employees.id=Activities.activator_id
                            LEFT OUTER JOIN Products ON Activities.product_id=Products.id)
                            GROUP BY Employees.name
                            ORDER BY Employees.name ASC
                    """)
        # COALESCE will put 0 if the SUM won't be calculated - replacing None in 0


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
