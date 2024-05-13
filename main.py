#run this using the shell command "streamlit run main.py" and then select show the web content

#to edit database, go to shell and run sqlite3 then .open general_ledger.db

import sqlite3
import pandas as pd
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
  connection = sqlite3.connect("general_ledger.db")
  cursor = connection.cursor()
  st.title("Wolaa!")
  entry_tab, acct_tab, report_tab = st.tabs(
      ["📝 New Entry", "✍ New Account", "📈 Reporting"])

  #loading this at the top level since it could be referenced in multiple locations
  coa_data = cursor.execute(
      "SELECT account_num, account_name, account_type FROM accounts ORDER BY account_num"
  ).fetchall()
  df_coa = pd.DataFrame(coa_data).rename(columns={0: "Number",1: "Name",2: "Type"})

  #Entry 
  with entry_tab:
    with st.form(key="new_je_form", clear_on_submit=True, border=False):
      st.header("Add Journal Entry")
      e_date = st.date_input("Posting Date")
      entry_tab_left, entry_tab_right = st.columns(2)
      account_options = [x[0] + " - " + x[1] for x in coa_data]
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

      submit_entry = st.form_submit_button("Post Entry")
      if submit_entry:
        if d_amt + c_amt == 0:
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
        if d_amt + c_amt != 0:
          print(entry_tab.write(f"Entry out of balance by {d_amt + c_amt}"))
        connection.commit()

  #new account tab
  with acct_tab:
    st.header("Add New General Ledger Account")
    with st.form("new_acct_form", clear_on_submit=True, border=False):
      acct_no = st.text_input("Account Number","")
      acct_name = st.text_input("Account Name","")
      acct_type = st.multiselect("Account Type", [
          "Current Assets", "Fixed Assets", "Long-Term Assets",
          "Current Liabilities", "Long-term Liabilities", "Equity", "Revenue",
          "Cost of Sales", "Expenses"
      ],
                                 max_selections=1)
      submit = st.form_submit_button("Add Account")
      if submit:
        cursor.execute(
            "INSERT INTO accounts (account_num, account_name, account_type) VALUES (?,?,?)",
            (acct_no, acct_name, acct_type[0]))
        connection.commit()

  with report_tab:
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
        info_tb = cursor.execute(
            f"SELECT date, account, SUM(amount) as balance FROM entries WHERE DATE(date) <= '{str(tb_date)}' GROUP BY account HAVING balance IS NOT NULL").fetchall(
            )
        entries_df = pd.DataFrame(info_tb).rename(columns={0:"Date", 1:"Acct No", 2: "Balance"})
        # df.loc['total'] = df.sum()
        # df.loc[df.index[-1], "Acct No"] = 'Total'
        # df.loc[df.index[-1], "Account Name"] = ''
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

  connection.close()


if __name__ == "__main__":
#   setup_function()
  streamlit_function()