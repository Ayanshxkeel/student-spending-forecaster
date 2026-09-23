import csv
import sqlite3
from datetime import date, timedelta
from io import StringIO


def connect(path="spending.db"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, day TEXT NOT NULL, merchant TEXT NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL)")
    db.commit()
    return db


def add(db, day, merchant, category, amount):
    date.fromisoformat(day)
    if not merchant.strip() or amount <= 0:
        raise ValueError("Enter a merchant and an amount above zero.")
    db.execute("INSERT INTO transactions(day,merchant,category,amount) VALUES (?,?,?,?)", (day, merchant.strip(), category.strip(), round(amount, 2)))
    db.commit()


def import_csv(db, content):
    reader = csv.DictReader(StringIO(content))
    if not {"date", "merchant", "category", "amount"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV needs date, merchant, category, amount columns.")
    existing = {(row[0], row[1], row[2], row[3]) for row in db.execute("SELECT day,merchant,category,amount FROM transactions")}
    added = 0
    for row in reader:
        day, merchant, category, amount = row["date"], row["merchant"], row["category"], float(row["amount"])
        key = (day, merchant.strip(), category.strip(), round(amount, 2))
        if key not in existing:
            add(db, *key)
            existing.add(key)
            added += 1
    return added


def transactions(db):
    return db.execute("SELECT day,merchant,category,amount FROM transactions ORDER BY day DESC,id DESC").fetchall()


def forecast(rows, today, budget):
    month_start = today.replace(day=1)
    month_rows = [row for row in rows if month_start <= date.fromisoformat(row[0]) <= today]
    spent = sum(row[3] for row in month_rows)
    days_elapsed = today.day
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    days_in_month = (next_month - month_start).days
    remaining = days_in_month - days_elapsed
    pace = spent / days_elapsed
    projected = spent + pace * remaining
    return round(spent, 2), round(projected, 2), round(budget - projected, 2), round(pace, 2)
