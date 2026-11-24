'''
Row-level chunking: one free-text chunk per order row, with the customer
details denormalized in (orders LEFT JOIN customers).
'''
import sqlite3

import pandas as pd

from tables.sql_query_tools import DB_PATH

# The joining below could also be done on direct csv data, but its best to do it on DB,
# to mimic real use case setting
JOIN_SQL = """
SELECT o.*,
       c.full_name, c.email, c.phone, c.city, c.state,
       c.loyalty_tier, c.registered_date
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""


def _has(value):
    return not (value is None or value == "" or pd.isna(value))


def row_to_text(r):
    """Serialize one joined order row into a short free-text description."""
    parts = [
        f"Order {r.order_id} (invoice {r.invoice_id}) placed on {r.order_date} "
        f"by {r.full_name} ({r.email}), a {r.loyalty_tier} member from {r.city}, {r.state}. "
        f"Status: {r.order_status}. "
        f"Items: {r.quantity} x {r.product_name} (model {r.model_number}). "
        f"Total: ${r.total_usd:.2f} (incl. ${r.tax_usd:.2f} tax), paid by {r.payment_method}."
    ]
    if _has(r.delivery_date):
        parts.append(f"Delivered on {r.delivery_date}.")
    if _has(r.warranty_expiry):
        parts.append(f"Warranty expires {r.warranty_expiry}.")
    if _has(r.return_reason):
        parts.append(
            f"Return requested on {r.return_requested_date}: {r.return_reason}."
        )
    if _has(r.refund_status) and r.refund_status != "N/A":
        refund = f"Refund status: {r.refund_status}"
        if _has(r.refund_amount_usd) and r.refund_amount_usd:
            refund += f", amount ${r.refund_amount_usd:.2f}"
        if _has(r.refund_date):
            refund += f", on {r.refund_date}"
        parts.append(refund + ".")
    if _has(r.support_notes):
        parts.append(f"Notes: {r.support_notes}")
    return " ".join(parts)


def build_order_customer_chunks_from_table():
    """Join orders with customers, then return one chunk per order row."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql(JOIN_SQL, conn)
    finally:
        conn.close()

    chunks = []
    for _, r in df.iterrows():
        chunks.append({
            "text": row_to_text(r),
            "metadata": {
                "source": "orders",
                "order_id": str(r.order_id),
                "customer_id": str(r.customer_id),
                "status": r.order_status,
                "order_date": str(r.order_date),
            },
        })
    return chunks


