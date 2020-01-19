import os
import sys
import repository

# Initiate the repository
if os.path.isfile('moncafe.db'):
    os.remove('moncafe.db')  # Removing the old db
repository.repo.__init__()

# Creating tables from repository
repository.repo.create_tables()

# Reading from config.txt
config = open(sys.argv[1])
line = config.readline()
while line:
    line = line.split(', ')  # line is an array now
    if line[0] == 'C':
        repository.repo.coffee_stands.insert(repository.Coffee_stand(line[1], line[2], line[3].splitlines()[0]))
    elif line[0] == 'S':
        repository.repo.suppliers.insert(repository.Supplier(line[1], line[2], line[3].splitlines()[0]))
    elif line[0] == 'E':
        repository.repo.employees.insert(repository.Employee(line[1], line[2], line[3], line[4].splitlines()[0]))
    elif line[0] == 'P':
        repository.repo.products.insert(repository.Product(line[1], line[2], line[3].splitlines()[0], 0))
    repository.repo._dbcon.commit()  # commit the changes
    line = config.readline()

config.close()