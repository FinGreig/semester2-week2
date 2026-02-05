import sqlite3

# ==================================================
# Section 1 – Summaries
# ==================================================

def total_customers(conn):
    cursor = conn.execute("""
    select count() as total_customers from customers
""")
    result = cursor.fetchone()
    print(f"Total Customers: {result['total_customers']}")


def customer_signup_range(conn):
    cursor = conn.execute("""
    select min(signup_date),max(signup_date) from customers
""")
    result = cursor.fetchone()
    print(f"Earliest Signup Date: {result[0]}")
    print(f"Latest Signup Date: {result[1]}")

def order_summary_stats(conn):
    cursor = conn.execute("""
    select count(),avg(order_total),min(order_total),max(order_total) from orders
""")
    result = cursor.fetchone()
    print(f"Total Orders: {result[0]}")
    print(f"Average Order Total: £{result[1]:.2f}")
    print(f"Minimum Order Total: £{result[2]:.2f}")
    print(f"Maximum Order Total: £{result[3]:.2f}")

def driver_summary(conn):
    cursor = conn.execute("""
    select count() from drivers
""")
    result = cursor.fetchone()
    print(f"Total Drivers: {result[0]}")
    cursor = conn.execute("""
    select driver_name,hire_date from drivers
""")
    for driver in cursor.fetchall():
        print(f"Driver: {driver['driver_name']:<25} Hire Date: {driver['hire_date']}")


# ==================================================
# Section 2 – Key Statistics
# ==================================================

def orders_per_customer(conn):
    cursor = conn.execute("""
    select customer_name,count() as orders, sum(order_total) as total_spent from orders
    left join customers on orders.customer_id = customers.customer_id
    group by orders.customer_id
""")
    for customer in cursor.fetchall():
        print(f"Customer: {customer['customer_name']:<25} Orders: {customer['orders']:<10} Total Spent: £{f'{customer['total_spent']:.2f}':<15}")


def driver_workload(conn):
    cursor = conn.execute("""
    select driver_name,count() as deliveries from deliveries
    right join drivers on deliveries.driver_id = drivers.driver_id
    group by drivers.driver_id
""")
    for driver in cursor.fetchall():
        print(f"Driver: {driver['driver_name']:<25} Deliveries: {driver['deliveries']}")


def delivery_lookup_by_id(conn, order_id):
    cursor = conn.execute("""
    select customer_name,order_total,delivery_date,driver_name from orders
    left join customers on orders.customer_id=customers.customer_id
    left join deliveries on orders.order_id=deliveries.order_id
    left join drivers on deliveries.driver_id=drivers.driver_id
    where orders.order_id=?
""",(order_id,))
    result = cursor.fetchone()
    if result:
        print(f"Customer Name: {result['customer_name']}")
        print(f"Order Total: £{result['order_total']:.2f}")
        print(f"Delivery Date: {result['delivery_date']}")
        print(f"Driver Name: {result['driver_name']}")
    else:
        print(f"No delivery found for Order ID: {order_id}")


# ==================================================
# Section 3 – Time-based Summaries
# ==================================================

def orders_per_date(conn):
    pass


def deliveries_per_date(conn):
    pass


def customer_signups_per_month(conn):
    pass


# ==================================================
# Section 4 – Performance and Rankings
# ==================================================

def top_customers_by_spend(conn, limit=5):
    pass


def rank_drivers_by_deliveries(conn):
    pass


def high_value_orders(conn, threshold):
    pass


# ==================================================
# Menus - You should not need to change any code below this point until the stretch tasks.
# ==================================================

def section_1_menu(conn):
    while True:
        print("\nSection 1 – Summaries")
        print("1. Total number of customers")
        print("2. Customer signup date range")
        print("3. Order summary statistics")
        print("4. Driver summary")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            total_customers(conn)
        elif choice == "2":
            customer_signup_range(conn)
        elif choice == "3":
            order_summary_stats(conn)
        elif choice == "4":
            driver_summary(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_2_menu(conn):
    while True:
        print("\nSection 2 – Key Statistics")
        print("1. Orders per customer")
        print("2. Driver workload")
        print("3. Order delivery overview")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_customer(conn)
        elif choice == "2":
            driver_workload(conn)
        elif choice == "3":
            order_id = input("Enter order ID: ").strip()
            if not order_id.isdigit():
                print("Please enter a valid integer order ID.")
                continue
            delivery_lookup_by_id(conn, int(order_id))
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_3_menu(conn):
    while True:
        print("\nSection 3 – Time-based Summaries")
        print("1. Orders per date")
        print("2. Deliveries per date")
        print("3. Customer signups per month")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_date(conn)
        elif choice == "2":
            deliveries_per_date(conn)
        elif choice == "3":
            customer_signups_per_month(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_4_menu(conn):
    while True:
        print("\nSection 4 – Performance and Rankings")
        print("1. Top 5 customers by total spend")
        print("2. Rank drivers by deliveries completed")
        print("3. High-value orders")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            top_customers_by_spend(conn)
        elif choice == "2":
            rank_drivers_by_deliveries(conn)
        elif choice == "3":
            try:
                threshold = float(input("Enter order value threshold (£): "))
                high_value_orders(conn, threshold)
            except:
                print("Please enter a valid numerical value.")
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def main_menu(conn):
    while True:
        print("\n=== Delivery Service Management Dashboard ===")
        print("1. Section 1 – Summaries")
        print("2. Section 2 – Key Statistics")
        print("3. Section 3 – Time-based Summaries")
        print("4. Section 4 – Performance and Rankings")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            section_1_menu(conn)
        elif choice == "2":
            section_2_menu(conn)
        elif choice == "3":
            section_3_menu(conn)
        elif choice == "4":
            section_4_menu(conn)
        elif choice == "0":
            print("Exiting dashboard.")
            break
        else:
            print("Invalid option. Please try again.")

def get_connection(db_path="food_delivery.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    conn = get_connection()
    main_menu(conn)
    conn.close()