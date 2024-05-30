import streamlit as st
import sqlite3
from streamlit_extras.stylable_container import stylable_container
import pandas as pd

st.set_page_config(
    page_title="Reports",
    page_icon="📈",
)

connection = sqlite3.connect("general_ledger.db")
cursor = connection.cursor()
df_coa = pd.DataFrame(st.session_state.coa_data).rename(columns={0: "Number",1: "Name",2: "Type"}) 

st.header("Reporting")
report_option = st.selectbox("Select your Report",("", "Journal Entries", "Chart of Accounts", "Trial Balance"))
  
#JE report
if report_option == "Journal Entries":
    st.header("Posted Journal Entries")
    request_journal_report = st.button("Load Entries", key="JL_Run_Report")
    if request_journal_report:
        info = cursor.execute(
        "SELECT ROWID, entry_no, date, account, amount FROM entries"
        ).fetchall()
        df_coa = pd.DataFrame(info).rename(columns={0: "Line No", 1: "Entry No", 2:"Posting Date", 3: "Account", 4: "Amount"})
        st.dataframe(df_coa,
                    column_config={"Amount": st.column_config.NumberColumn("Amount", format="%.2f", help="Line Amount")},
                    use_container_width=True,
                    hide_index=True)

#COA report
if report_option == "Chart of Accounts":    
    st.header("Company Chart of Accounts")
    st.dataframe(df_coa,
                    use_container_width=True,
                    hide_index=True)

#TB report
if report_option == "Trial Balance":
    tb_date = st.date_input("Report Date", key="TB_D")
    get_tb = st.button("Run Trial Balance", key="TB_run")
    if get_tb:
        st.header("Company Trial Balance")
        st.subheader(f"(As of {tb_date})")
        info_tb = cursor.execute(f"SELECT date, account, SUM(amount) as balance FROM entries WHERE DATE(date) <= '{str(tb_date)}' GROUP BY account HAVING balance IS NOT NULL").fetchall()
        entries_df = pd.DataFrame(info_tb).rename(columns={0:"Date", 1:"Acct No", 2: "Balance"})

        tb_df = entries_df.merge(df_coa, how='left', left_on="Acct No", right_on="Number")
        tb_df = tb_df[["Acct No", "Name", "Type", "Balance"]]

        # should check if it balances, otherwise return error
        st.dataframe(tb_df,
                    column_config={"Balance": st.column_config.NumberColumn("Account Balance", format="%.2f", help="balance at date")},
                    use_container_width=True,
                    hide_index=True)

# get_cash = st.button("Run Cash Chart", key="cash_run")
# if get_cash:
#   cash_info = cursor.execute(f"SELECT date, amount, account FROM entries where account = '1000'").fetchall()
#   cash_df = pd.DataFrame(cash_info).rename(columns={0: "Date", 1: "Amount", 2:"Account"})
#   st.line_chart(cash_df, x="Date", y="Amount")

#   cs = cash_df[["Date", "Amount"]]
#   cs = cs.sort_values(by=["Date"]).cumsum()

#   ytd = cash_df.merge(cs, how='left', left_index=True, right_index=True).sort_values(by=["Date_x"])
#   st.line_chart(ytd, x="Date_x", y="Amount_y")