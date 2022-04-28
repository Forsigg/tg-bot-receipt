import sqlite3


def write_receipt_to_db(receipt_name):
    conn = sqlite3.connect('rec_db.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO receipts VALUES ('{receipt_name}')")
    conn.commit()
    conn.close()


def is_receipt_in_db(receipt_name):
    conn = sqlite3.connect('rec_db.db')
    cur = conn.cursor()
    receipt = list(cur.execute(f"SELECT * FROM receipts WHERE name='{receipt_name}'"))
    if receipt:
        conn.close()
        return True
    conn.close()
    return False