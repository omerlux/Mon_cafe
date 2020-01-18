import os
import sqlite3
import sys

class _main:

    # Creation of a new database
    os.remove('moncafe.db')  # Removing the old db
    dbcon = sqlite3.connect('moncafe.db')
    cursor = dbcon.cursor()
    # Employees table
    cursor.execute("""CREATE TABLE Employees (
                           id INTEGER PRIMARY KEY, 
                           name TEXT NOT NULL, 
                           salary REAL NOT NULL, 
                           coffee_stand INTEGER REFERENCES Coffee_stands(id))""")
    # Suppliers table
    cursor.execute("""CREATE TABLE Suppliers(
                           id INTEGER PRIMARY KEY,
                           name TEXT NOT NULL,
                           contact_information TEXT)""")
    # Products table
    cursor.execute("""CREATE TABLE Products(
                           id INTEGER PRIMARY KEY,
                           description TEXT NOT NULL,
                           price REAL NOT NULL,
                           quantity INTEGER NOT NULL)""")
    # Coffee_stand table
    cursor.execute("""CREATE TABLE Coffee_stands(
                           id INTEGER PRIMARY KEY,
                           location TEXT NOT NULL,
                           number_of_employees INTEGER)""")
    # Activities table
    cursor.execute("""CREATE TABLE Activities(
                           product_id INTEGER INTEGER REFERENCES Product(id),
                           quantity INTEGER NOT NULL,
                           activator_id INTEGER NOT NULL,
                           date DATE NOT NULL)""")

    # Reading from config.txt
    config = open(sys.argv[1])
    line = config.readline()
    while line:
        cursor.execute("INSERT INTO Coffee_stands VALUES (1,'asd',3)")
        dbcon.commit()

        line = line.split(', ')     # line is an array now
        if line[0] == 'C':
            cursor.execute("""
                         INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?,?,?)
                         """, (line[1], line[2], line[3].splitlines()[0]))
            dbcon.commit()
        if line[0] == 'S':
            cursor.execute("""
                        INSERT INTO Suppliers (id, name, contact_information) VALUES (?,?,?)
                        """, (line[1], line[2], line[3].splitlines()[0]))
        if line[0] == 'E':
            cursor.execute("""
                      INSERT INTO Employees (id, name, salary, coffee_stand) VALUES (?,?,?,?)
                      """, (line[1], line[2], line[3], line[4].splitlines()[0]))
        if line[0] == 'P':
            cursor.execute("""
                        INSERT INTO Products (id, description, price, quantity) VALUES (?,?,?,?)
                        """, (line[1], line[2], line[3].splitlines()[0], 0))
        line = config.readline()

    config.close()

#    def activitie_insert(self, line):
#        self.cursor.execute("""
#            INSERT INTO Coffee_stands (product_id, quantity, activator_id, date) VALUE (?,?,?)
#            """, [line[1], line[2], line[3]], line[4])