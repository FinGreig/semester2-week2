"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3


def customer_tickets(conn, customer_id):
    """
    Return a list of tuples:
    (film_title, screen, price)

    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """
    cursor = conn.execute("""
    select title as film_title,screen,price
    from screenings as s
    inner join films as f on s.film_id=f.film_id
    inner join tickets as t on s.screening_id=t.screening_id
    where t.customer_id = ?
    order by film_title asc
    """,(customer_id,))
    return cursor.fetchall()


def screening_sales(conn):
    """
    Return a list of tuples:
    (screening_id, film_title, tickets_sold)

    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """
    cursor = conn.execute("""
    select s.screening_id,title as film_title,count(ticket_id) as tickets_sold
    from screenings as s
    inner join films as f on s.film_id=f.film_id
    left join tickets as t on s.screening_id=t.screening_id
    group by s.screening_id
    order by tickets_sold desc
    """)
    return cursor.fetchall()


def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples:
    (customer_name, total_spent)

    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """
    cursor = conn.execute("""
    select customer_name,sum(t.price) as total_spent
    from customers as c
    inner join tickets as t on c.customer_id=t.customer_id
    group by c.customer_id
    order by total_spent desc,customer_name asc
    limit ?
    """,(limit,))
    return cursor.fetchall()