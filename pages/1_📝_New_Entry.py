import streamlit as st
import sqlite3
import pandas as pd
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(
    page_title="New Entry",
    page_icon="📝",
)

#should I define this in every page, or once at the top level and then add it to session state
connection = sqlite3.connect("general_ledger.db")
cursor = connection.cursor()

with st.form(key="new_je_form", clear_on_submit=True, border=False):

    st.header(cursor.execute(f"SELECT company_name from company_settings").fetchall()[0][0])
    st.subheader("Add Journal Entry")
    
    e_date = st.date_input("Posting Date")
    entry_tab_left, entry_tab_right = st.columns(2)
    account_options = [x[0] + " - " + x[1] for x in st.session_state.coa_data]
    with entry_tab_left:
        d_acct = st.multiselect(
            "Debit Account",
            account_options,
            max_selections=1,
            key="dact")
        d_amt = st.number_input("Debit Amount")

    with entry_tab_right:
        c_acct = st.multiselect(
            "Credit Account",
            account_options,
            max_selections=1)
        c_amt = st.number_input("Credit Amount")
    with stylable_container(key="Test_button", css_styles="button { border: 1px solid rgb(0,255,0,0.2); background-color: green; color: white; border-radius: 20px}"):
        submit_entry = st.form_submit_button("Post Entry")
        if submit_entry:
            if d_amt + c_amt == 0 and st.session_state.block_posting == False:
                previous_entry_no = cursor.execute("SELECT MAX(entry_no) from entries").fetchall()[0][0]
                if previous_entry_no:
                    next_entry_no = previous_entry_no + 1 
                else:
                    next_entry_no = 1
            
                cursor.execute(
                    "INSERT INTO entries (entry_no, date, account, amount) VALUES (?,?,?,?)",
                    (next_entry_no, e_date, d_acct[0].split(" - ")[0], d_amt))
                cursor.execute(
                    "INSERT INTO entries (entry_no, date, account, amount) VALUES (?,?,?,?)",
                    (next_entry_no, e_date, c_acct[0].split(" - ")[0], c_amt))
            if st.session_state.block_posting == True:
                st.write(f"G/L Posting is locked, please see settings")
            if d_amt + c_amt != 0:
                print(st.write(f"Entry out of balance by {d_amt + c_amt}"))
            connection.commit()