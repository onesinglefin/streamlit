import streamlit as st
import pandas as pd
import sqlite3
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(
    page_title="New Account",
    page_icon="✍",
)

connection = sqlite3.connect("general_ledger.db")
cursor = connection.cursor()

st.header(cursor.execute(f"SELECT company_name from company_settings").fetchall()[0][0])
st.subheader("Add New General Ledger Account")

with st.form("new_acct_form", clear_on_submit=True, border=False):
    acct_no = st.text_input("Account Number","")
    acct_name = st.text_input("Account Name","")
    acct_type = st.multiselect("Account Type", [
        "Current Assets", "Fixed Assets", "Long-Term Assets",
        "Current Liabilities", "Long-term Liabilities", "Equity", "Revenue",
        "Cost of Sales", "Expenses"
    ],
                                max_selections=1)
    with stylable_container(key="Test_button", css_styles="button { border: 1px solid rgb(49,51,63,0.2); background-color: green; color: white; border-radius: 20px}"):
        submit = st.form_submit_button("Add Account")
        if submit:
            if acct_no not in pd.DataFrame(st.session_state.coa_data)[0].values:
                cursor.execute(
                    "INSERT INTO accounts (account_num, account_name, account_type) VALUES (?,?,?)",
                    (acct_no, acct_name, acct_type[0]))
                connection.commit()
                # rerun the COA data to session state

            else:
                st.write("This account number is already in use")