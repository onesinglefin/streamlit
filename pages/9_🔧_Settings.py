import streamlit as st
import sqlite3
from streamlit_extras.stoggle import stoggle
from streamlit_extras.badges import badge
from streamlit_extras.bottom_container import bottom
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(
    page_title="Settings",
    page_icon="🔧",
)

connection = sqlite3.connect("general_ledger.db")
cursor = connection.cursor()

st.header(st.session_state.co_name)
st.subheader("Company Settings")

account_options = [x[0] for x in st.session_state.coa_data]

with st.form("settings_form", clear_on_submit=True):

    ar_acct = st.multiselect(
                "AR Account",
                account_options,
                default="1200",
                max_selections=1,
                key="ar_option")

    ar_acct = st.multiselect(
                "AP Account",
                account_options,
                default="2200",
                max_selections=1,
                key="ap_option")
    
    block_posting = st.toggle("Lock Posting", value=st.session_state.block_posting)

    with stylable_container(key="update_settings", css_styles="button { border: 1px solid rgb(49,51,63,0.2); background-color: green; color: white; border-radius: 20px}"):
        submit = st.form_submit_button("Update Settings")
        if submit:
            cursor.execute(
                "SELECT * from company_settings")
            # connection.commit()
            st.rerun()
            # rerun the COA data to session state


    


st.markdown("""
            
                - Create company information table
                - Put reports page in a form? 
                - Add widgets for KPIs to main page
            """
            
            
            )

with bottom():
    stoggle("Company Information", "Wolaa, the world's lamest accounting application, is a wholy-owned subsidiary of World Domination Incorporated (WDI)")
    stoggle("Disclaimer", "World Domination Incorporated and its subsidiaries are not responsible for anything. Ever. Don't ask again.")
    badge(type="github", name="onesinglefin/streamlit")