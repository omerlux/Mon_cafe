import repository

# print with ORM
def print_a_list(list):
    for item in list:
        print(item)


# print with corsur.execute
def print_row_row(cursor):
    for row in cursor:
        print(row)


if __name__ == '__main__':

    # Print Activities
    print("Activities")
    repository.repo.activities.print()

    # Print Coffee Stands
    print("Coffee stands")
    repository.repo.coffee_stands.print()

    # Print Employees - normal
    print("Employees")
    repository.repo.employees.print()

    # Print Products
    print("Products")
    repository.repo.products.print()

    # Print Suppliers
    print("Suppliers")
    repository.repo.suppliers.print()
    print()

    # Print Employees Report
    print("Employees report")
    repository.repo.get_employees_report()

    # Print Activities - complex
    repository.repo.get_extra_activities()