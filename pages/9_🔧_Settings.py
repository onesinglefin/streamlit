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
            
                  - Can I put the settings at the end or will I *always* run into the referenced before assignment error? Likely need to store in db and retrieve to session state
                  - Need to validate that an account number isn't already in use before trying to add it
                  - Create company information table
                  - Add widgets for KPIs to main page
            """
            
            
            )
stoggle("Company Information", "Blah Blah Blah")
stoggle("Disclaimer", "Don't blame me")
with bottom():
    badge(type="github", name="onesinglefin/streamlit")