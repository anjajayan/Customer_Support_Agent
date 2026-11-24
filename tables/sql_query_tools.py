'''
Read-only query tools over the local customer_support.db (tables: customers, orders).
All queries are parameterized to avoid SQL injection.
'''
import sqlite3
from pathlib import Path

# Resolve the DB relative to the working directory used by upload_to_db.py;
# fall back to the folder containing this file.
_DEFAULT_DB = Path("customer_support.db")
DB_PATH = _DEFAULT_DB if _DEFAULT_DB.exists() else Path(__file__).parent / "customer_support.db"


def _query(sql, params=()):
    """Run a SELECT and return a list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def get_order(order_id):
    """Return a single order (dict) by order_id, or None if not found."""
    rows = _query("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    return rows[0] if rows else None


def get_customer_by_email(email):
    """Return a single customer (dict) by email (case-insensitive), or None."""
    rows = _query(
        "SELECT * FROM customers WHERE LOWER(email) = LOWER(?)", (email.strip(),)
    )
    return rows[0] if rows else None


def list_orders(customer_id, status=None, since=None):
    """
    List a customer's orders, newest first.

    status: optional order_status filter (e.g. 'Processing', 'Shipped', 'Delivered'), case-insensitive.
    since:  optional ISO date string 'YYYY-MM-DD'; only orders on/after this date.
    """
    sql = "SELECT * FROM orders WHERE customer_id = ?"
    params = [customer_id]
    if status:
        sql += " AND LOWER(order_status) = LOWER(?)"
        params.append(status)
    if since:
        sql += " AND order_date >= ?"
        params.append(since)
    sql += " ORDER BY order_date DESC"
    return _query(sql, params)


def customer_order_summary(customer_id):
    """
    Return a summary for a customer: profile, order count, total spend,
    refunded amount, first/last order dates and a count of orders per status.
    Returns None if the customer does not exist.
    """
    customers = _query("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
    if not customers:
        return None

    totals = _query(
        """
        SELECT COUNT(*)                          AS order_count,
               COALESCE(SUM(total_usd), 0)       AS total_spent_usd,
               COALESCE(SUM(refund_amount_usd), 0) AS total_refunded_usd,
               MIN(order_date)                   AS first_order_date,
               MAX(order_date)                   AS last_order_date
        FROM orders WHERE customer_id = ?
        """,
        (customer_id,),
    )[0]

    by_status = _query(
        """
        SELECT order_status, COUNT(*) AS count
        FROM orders WHERE customer_id = ?
        GROUP BY order_status
        """,
        (customer_id,),
    )

    return {
        "customer": customers[0],
        **totals,
        "orders_by_status": {r["order_status"]: r["count"] for r in by_status},
    }



    
