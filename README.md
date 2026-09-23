# Student Spending Forecaster

Record purchases, view category totals, and estimate where this month's spending pace could end.

## Features

- Adds purchases with date, merchant, category, and amount.
- Imports a CSV and skips rows already present in the local database.
- Displays spending history and totals by category.
- Compares a month-end projection with a monthly budget.

## Run locally

```bash
git clone https://github.com/Ayanshxkeel/student-spending-forecaster.git
cd student-spending-forecaster
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On Windows, activate with `.venv\Scripts\activate`.

## Try it

Import `sample_transactions.csv`, set a budget, and inspect the purchase table and category chart. Import the same file again: identical rows should be skipped. The sample dates are in September 2026, so its purchases count toward the current-month projection only during that month.

## CSV format and logic

Use columns `date,merchant,category,amount`, ISO dates (`YYYY-MM-DD`), and positive expenses. `logic.py` saves rows in SQLite. `forecast()` divides month-to-date spending by elapsed days, then extends that daily average to month end. `app.py` renders the form, metrics, chart, and table.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Spending tracker interface |
| `logic.py` | SQLite storage, import, and projection |
| `sample_transactions.csv` | Example purchases |
| `requirements.txt` | Python dependencies |

## Data and limitations

Your transactions stay in local `spending.db`. Stop the app and delete it to reset. This is a **spending-rate extrapolation**, not an ML prediction. It does not account for scheduled rent, refunds, or seasonal changes. Do not import account credentials.
