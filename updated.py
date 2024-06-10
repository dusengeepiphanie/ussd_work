from flask import Flask, request, Response
import mysql.connector
import re


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Milk_stores"
    )

def is_valid_phone(phone):
    return bool(re.match(r"^(079|078)\d{7}$", phone))

def is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def is_valid_pin(pin):
    return bool(re.match(r"^\d{5}$", pin))

def register_customer():
    connection = connect_db()
    cursor = connection.cursor()
    
    print("Customer Registration")

    while True:
        email = input("Enter your email: ")
        if is_valid_email(email):
            break
        else:
            print("Invalid email format. Please enter a valid email.")
    
    while True:
        phone = input("Enter your phone number: ")
        if is_valid_phone(phone):
            break
        else:
            print("Invalid phone number. It must be 10 digits long and start with 079 or 078.")
    
    while True:
        pin = input("Enter a PIN: ")
        if is_valid_pin(pin):
            break
        else:
            print("Invalid PIN. It must be exactly 5 digits long and contain only numbers.")
    
    road_nbr = input("Enter your road number: ")

    cursor.execute(
        "INSERT INTO Customers (Email, Phone, PIN, Road_nbr) VALUES (%s, %s, %s, %s)",
        (email, phone, pin, road_nbr)
    )
    connection.commit()
    print("Registration successful!")
    cursor.close()
    connection.close()

def login_customer():
    connection = connect_db()
    cursor = connection.cursor()

    print("Customer Login")
    while True:
        phone = input("Enter your phone number: ")
        if is_valid_phone(phone):
            break
        else:
            print("Invalid phone number. It must be 10 digits long and start with 079 or 078.")
    
    pin = input("Enter your PIN: ")

    cursor.execute("SELECT C_id FROM Customers WHERE Phone = %s AND PIN = %s", (phone, pin))
    result = cursor.fetchone()
    
    if result:
        customer_id = result[0]
        print("Login successful!")
        cursor.close()
        connection.close()
        return customer_id
    else:
        print("Invalid phone number or PIN. Please try again.")
        cursor.close()
        connection.close()
        return None

def place_order(customer_id):
    connection = connect_db()
    cursor = connection.cursor()

    print("WELCOME TO MUKAMIRA DIARY LTD")
    print("1. Place Order")
    print("2. Available Products")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == '3':
        print("Exiting...")
        return

    

    # Step 2: Select a product
    print("SELECT A PRODUCT:\n")
    cursor.execute("SELECT P_name FROM products")
    products = cursor.fetchall()

    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product[0]}")

    product_choice = int(input("Choose a product: ")) - 1
    selected_product = products[product_choice][0]

    # Step 3: Select a size
    print("SELECT SIZE")
    sizes = ["250 ml", "1L", "3L"]
    for idx, size in enumerate(sizes, start=1):
        print(f"{idx}. {size}")

    size_choice = int(input("Choose a size: ")) - 1
    selected_size = sizes[size_choice]

    # Step 4: Confirm order
    order_amount = int(input("Enter Order amount: "))
    cursor.execute("SELECT P_unitprice FROM products WHERE P_name = %s", (selected_product,))
    unit_price = cursor.fetchone()[0]
    total_price = order_amount * unit_price

    print("Confirm Order:")
    print(f"Product_Name: {selected_product}")
    print(f"Size: {selected_size}")
    print(f"Order_Amount: {order_amount}")
    print(f"Total_Price: {total_price}")
    print("1. Confirm")
    print("2. Cancel")

    final_choice = input("Choose an option: ")
    if choice == '2':
        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()
        for i in data:
            print(f"ID: {i[0]}, Name: {i[1]}, Size: {i[2]}, Price: {i[3]}")
        return

    if final_choice == '1':
        cursor.execute(
            "INSERT INTO Orders (C_id, Order_amount, Order_totalprice) VALUES (%s, %s, %s)",
            (customer_id, order_amount, total_price)
        )
        connection.commit()
        print("Order placed successfully!")
    else:
        print("Order cancelled.")

    cursor.close()
    connection.close()

def main():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register_customer()
        elif choice == '2':
            customer_id = login_customer()
            if customer_id:
                place_order(customer_id)
                break 
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
