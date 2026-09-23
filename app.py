from datetime import date
import pandas as pd
import streamlit as st
from logic import add, connect, forecast, import_csv, transactions

st.set_page_config(page_title="Student Spending Forecaster", page_icon="💸", layout="wide")
st.title("Student Spending Forecaster")
st.caption("Track your actual spending and see where this month's pace is taking you.")
db = connect()
with st.form("new_transaction"):
    st.subheader("Add a purchase")
    a, b, c, d = st.columns(4)
    day = a.date_input("Date", date.today())
    merchant = b.text_input("Merchant")
    category = c.selectbox("Category", ["Groceries", "Food", "Transport", "Housing", "School", "Other"])
    amount = d.number_input("Amount ($)", 0.01, 100000.0, 10.0, 0.01)
    if st.form_submit_button("Save purchase"):
        try:
            add(db, str(day), merchant, category, amount)
            st.success("Purchase saved.")
        except ValueError as error:
            st.error(str(error))
with st.expander("Import purchases from CSV"):
    st.write("Columns: date, merchant, category, amount. Positive amounts are expenses. Re-importing identical rows skips duplicates.")
    uploaded = st.file_uploader("Choose CSV", type="csv")
    if uploaded and st.button("Import CSV"):
        try:
            count = import_csv(db, uploaded.read().decode("utf-8-sig"))
            st.success(f"Imported {count} new purchases.")
        except (ValueError, UnicodeDecodeError) as error:
            st.error(str(error))
rows = transactions(db)
budget = st.number_input("Monthly budget ($)", 1.0, 100000.0, 1000.0, 10.0)
spent, projected, remaining, pace = forecast(rows, date.today(), budget)
c1, c2, c3 = st.columns(3)
c1.metric("Spent this month", f"${spent:,.2f}")
c2.metric("Projected month end", f"${projected:,.2f}")
c3.metric("Projected budget difference", f"${remaining:,.2f}")
st.caption(f"Projection assumes your average daily spending so far (${pace:.2f}) continues through month end. It is a planning estimate, not an ML prediction.")
if rows:
    frame = pd.DataFrame(rows, columns=["Date", "Merchant", "Category", "Amount"])
    st.subheader("Spending by category")
    st.bar_chart(frame.groupby("Category")["Amount"].sum())
    st.subheader("Purchases")
    st.dataframe(frame, hide_index=True, width="stretch")
else:
    st.info("Add purchases or import the sample CSV to explore the dashboard.")
