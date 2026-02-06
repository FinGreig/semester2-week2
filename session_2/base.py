from select import select
import sqlite3
# you will need to pip install pandas matplotlib
import pandas as pd
import matplotlib as mpl

def get_connection(db_path="orders.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def list_product_categories(conn):
    """
    Returns a DataFrame of distinct product categories.

    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""select distinct category from products order by category asc""", conn))
    return df

def total_customers(conn):
    """
    Returns a DataFrame with the total number of customers.

    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""select count() as total_customers from customers""", conn))
    return df

def orders_by_customer(conn, email):
    """
    Returns a DataFrame of orders for a given customer email.
    
    :param conn: db connection
    :param email: customer email
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select o.order_id,o.order_date,o.status,o.total_amount from orders as o
    inner join customers as c on o.customer_id=c.customer_id
    where c.email=?
    order by o.order_date desc
    """, conn, params=(email,)))
    return df

def products_below_price(conn, price):
    """
    Returns a DataFrame of products priced below a given price.
    
    :param conn: db connection
    :param price: price threshold
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select name as product_name, category, price from products
    where price < ?
    """, conn, params=(price,)))
    return df

def total_spent_per_customer(conn):
    """
    Returns a DataFrame of total amount spent per customer.
    
    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select c.email as customer_email, sum(o.total_amount) as total_spent from customers as c
    inner join orders as o on c.customer_id=o.customer_id
    group by c.customer_id
    """, conn))
    return df

def orders_per_category(conn):
    """
    Returns a DataFrame of total orders per product category.
    
    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select distinct p.category, count(oi.order_item_id) as total_orders from products as p
    inner join order_items as oi on p.product_id=oi.product_id
    group by p.category
    """, conn))
    return df

def average_products_per_order(conn):
    """
    Returns a DataFrame of the average number of products per order.

    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select avg(order_item_count) as avg_products_per_order from (
        select o.order_id, sum(oi.quantity) as order_item_count from orders as o
        inner join order_items as oi on o.order_id=oi.order_id
        group by o.order_id
    )
    """, conn))
    return df

def deliveries_by_status(conn):
    """
    Plots a pie chart of deliveries by scheduled, delivered and failed
    
    :param conn: db connection
    """
    df = pd.DataFrame(pd.read_sql_query("""
    select delivery_status as status, count() as count from deliveries
    group by status
    """, conn))
    df.set_index("status", inplace=True)
    df.plot.pie(y="count", autopct="%1.1f%%", legend=False, title="Deliveries by Status")
    mpl.pyplot.show()

def menu(conn):
    while True:
        print("\n=== Leedsburies Supermarket Menu ===")
        print("1. List product categories")
        print("2. Total number of customers")
        print("3. Orders for a given customer")
        print("4. All products priced below £2")
        print("5. Total spent per customer")
        print("6. Orders per product category")
        print("7. Average number of products per order")
        print("8. Summarize deliveries by status")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            df = list_product_categories(conn)
            print(df.to_string(index=False))

        elif choice == "2":
            df = total_customers(conn)
            print(df.to_string(index=False))

        elif choice == "3":
            email = input("Enter customer email: ").strip()
            df = orders_by_customer(conn, email)
            if df.empty:
                print("No orders found for that email.")
            else:
                print(df.to_string(index=False))
        
        elif choice == "4":
            df = products_below_price(conn, 2.00)
            print(df.to_string(index=False))

        elif choice == "5":
            df = total_spent_per_customer(conn)
            print(df.to_string(index=False))

        elif choice == "6":
            df = orders_per_category(conn)
            print(df.to_string(index=False))

        elif choice == "7":
            df = average_products_per_order(conn)
            print(df.to_string(index=False))

        elif choice == "8":
            deliveries_by_status(conn)

        elif choice == "0":
            break

        else:
            print("Invalid option. Please try again.")

def main():

    db = get_connection()

    menu(db)

    db.close()


if __name__=="__main__":
    main()
