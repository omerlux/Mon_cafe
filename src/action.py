import sys
import repository

# Reading from config.txt
action = open(sys.argv[1])
line = action.readline()
while line:
    line = line.split(', ')  # line is an array now
    product_id_input = int(line[0])
    quantity_input = int(line[1])
    empsup_input = line[2]
    date_input = line[3].splitlines()[0]

    # check if the quantity+input_quantity is not negative
    new_quantity = repository.repo.products.quantity_check(product_id_input)[0] + quantity_input

    if new_quantity >= 0:
        repository.repo.products.update_quantity(product_id_input, new_quantity)
        repository.repo.activities.insert(repository.Activity(product_id_input, quantity_input, empsup_input, date_input))

    repository.repo._dbcon.commit()  # commit the changes
    line = action.readline()

action.close()