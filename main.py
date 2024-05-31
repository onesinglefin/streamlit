#run this using the shell command "streamlit run main.py" and then select show the web content

#to edit database, go to shell and run sqlite3 then .open general_ledger.db

import sqlite3
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from datetime import date, timedelta

def setup_function():
  connection = sqlite3.connect("general_ledger.db")
  cursor = connection.cursor()
  cursor.execute(
    "CREATE TABLE IF NOT EXISTS entries (entry_no INTEGER, date TEXT, account TEXT, amount REAL)"
  )
  cursor.execute(
    "CREATE TABLE IF NOT EXISTS accounts (account_num TEXT PRIMARY KEY, account_name TEXT, account_type TEXT)"
  )
  
  cursor.execute(
    "CREATE TABLE IF NOT EXISTS company_settings (company_name TEXT PRIMARY KEY, year_end_date TEXT, block_posting BOOL, ar_account TEXT, ap_account TEXT)"
  )

  cursor.execute(
    "CREATE TABLE IF NOT EXISTS customers (cust_name TEXT PRIMARY KEY, cust_address TEXT, cust_active BOOL)"
  )

  cursor.execute(
    "CREATE TABLE IF NOT EXISTS vendors (vend_name TEXT PRIMARY KEY, vend_address TEXT, vend_active BOOL)"
  )

  cursor.execute(
                    "INSERT INTO company_settings (company_name, year_end_date, block_posting, ap_account) VALUES (?,?,?,?)",
                    ("World Domination Inc", "2024-12-31", False, 2200))
  connection.commit()

def streamlit_function():

  st.set_page_config(
    page_title="Wolaa - The World's Lamest Accounting App!",
    page_icon="👋",
)
  
  # this should be stored in the database, and saved to session.
  block_posting = False
  if "block_posting" not in st.session_state:
    st.session_state.block_posting = block_posting

  connection = sqlite3.connect("general_ledger.db")
  cursor = connection.cursor()

  co_name = cursor.execute(f"SELECT company_name from company_settings").fetchall()[0][0]

  if "co_name" not in st.session_state:
    st.session_state.co_name = co_name

  #load coa and send to session state since it could be referenced in multiple locations
  coa_data = cursor.execute(
      "SELECT account_num, account_name, account_type FROM accounts ORDER BY account_num"
  ).fetchall()
  if "coa_data" not in st.session_state:
    st.session_state.coa_data = coa_data


  # st.header("Company Main Page")
  st.header(cursor.execute(f"SELECT company_name from company_settings").fetchall()[0][0])
  st.subheader("Company Main Page")

  todays_date = date.today()
  month_agos_date = todays_date - timedelta(days=30)

  #need to use cash account type instead of account 1000
  current_cash_bal = cursor.execute(f"SELECT date, account, SUM(amount) as balance FROM entries WHERE DATE(date) <= '{str(todays_date)}' AND account = '1000' GROUP BY account HAVING balance IS NOT NULL").fetchall()[0][-1]
  prior_cash_bal = cursor.execute(f"SELECT date, account, SUM(amount) as balance FROM entries WHERE DATE(date) <= '{str(month_agos_date)}' AND account = '1000' GROUP BY account HAVING balance IS NOT NULL").fetchall()[0][-1]
  st.metric("Cash Balance (30 day change)",current_cash_bal,prior_cash_bal-current_cash_bal)

  connection.close()

if __name__ == "__main__":
  # setup_function()
  streamlit_function()