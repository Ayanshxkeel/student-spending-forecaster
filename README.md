# Student Spending Forecaster

Track purchases, view category totals, and estimate your month-end total from your average daily spending so far.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Try it

Import `sample_transactions.csv` using the CSV section, then set a monthly budget. You should see purchase history, category totals, and a month-end projection. Import the same file again: identical rows are skipped.

For your own file, use columns `date,merchant,category,amount`, with ISO dates (`YYYY-MM-DD`) and positive amounts for expenses. Do not upload bank credentials. Data stays in local `spending.db`; delete it with the app stopped to reset. The sample dates are September 2026, so they only count toward the current month during September 2026. The projection is a simple spending-rate extrapolation; it does not account for upcoming rent or other scheduled costs.
