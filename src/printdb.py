import repository


def printit():
    # Print Activities
    print("Activities")
    act = repository.repo.activities.print()
    for item in act:
        tup = (item.product_id, item.quantity, item.activator_id, item.date)
        print(tup)

    # Print Coffee Stands
    print("Coffee stands")
    cs = repository.repo.coffee_stands.print()
    for item in cs:
        tup = (item.id, item.location, item.number_of_employees)
        print(tup)

    # Print Employees - normal
    print("Employees")
    emp = repository.repo.employees.print()
    for item in emp:
        tup = (item.id, item.name, item.salary, item.coffee_stand)
        print(tup)

    # Print Products
    print("Products")
    prod = repository.repo.products.print()
    for item in prod:
        tup = (item.id, item.description, item.price, item.quantity)
        print(tup)

    # Print Suppliers
    print("Suppliers")
    sup = repository.repo.suppliers.print()
    for item in sup:
        tup = (item.id, item.name, item.contact_information)
        print(tup)
    print()

    # Print Employees Report
    print("Employees report")
    emp_rep = repository.repo.get_employees_report()
    for item in emp_rep:
        print(item)  # special print

    # Print Activities - complex
    act_rep = repository.repo.get_extra_activities()
    if len(act_rep) != 0:
        print()
        print("Activities")
        for item in act_rep:
            tup = (item.date, item.description, item.quantity, item.name_emp, item.name_sup)
            print(tup)


if __name__ == '__main__':
    printit()
