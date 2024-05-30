#run this using the shell command "streamlit run main.py" and then select show the web content

#to edit database, go to shell and run sqlite3 then .open general_ledger.db

import sqlite3
import streamlit as st

def setup_function():
  connection = sqlite3.connect("general_ledger.db")
  cursor = connection.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS entries (entry_no INTEGER, date TEXT, account TEXT, amount REAL)"
  )
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS accounts (account_num TEXT PRIMARY KEY, account_name TEXT, account_type TEXT)"
  )


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



  #load coa and send to session state since it could be referenced in multiple locations
  coa_data = cursor.execute(
      "SELECT account_num, account_name, account_type FROM accounts ORDER BY account_num"
  ).fetchall()
  if "coa_data" not in st.session_state:
    st.session_state.coa_data = coa_data

  connection.close()

if __name__ == "__main__":
#   setup_function()
  streamlit_function()