import repository

# print with ORM
def print_a_list(list):
    for item in list:
        print(item)


# print with corsur.execute
def print_row_row(corsur):
    for row in corsur:
        print(row)


if __name__ == '__main__':
    # Print Activities
    print("Activities")
    toprint = repository.repo.activities.print()
    print_row_row(toprint)


    # Print Coffee Stands
    print("Coffee stands")
    toprint = repository.repo.coffee_stands.print()
    print_row_row(toprint)

    # Print Employees - normal
    print("Employees")
    toprint = repository.repo.employees.print()
    print_row_row(toprint)

    # Print Products
    print("Products")
    toprint = repository.repo.products.print()
    print_a_list(toprint)

    # Print Suppliers
    print("Suppliers")
    toprint = repository.repo.suppliers.print()
    print_row_row(toprint)
    print()

    # Print Employees Report
    print("Employees report")


    print()

    # Print Activities - complex
    print("Activities")
    cursor = repository.repo.get_extra_activities()
    print_row_row(cursor)
