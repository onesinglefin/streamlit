import streamlit as st
import sqlite3
from streamlit_extras.stoggle import stoggle
from streamlit_extras.badges import badge
from streamlit_extras.bottom_container import bottom

st.set_page_config(
    page_title="Settings",
    page_icon="🔧",
)

connection = sqlite3.connect("general_ledger.db")
cursor = connection.cursor()

st.header(cursor.execute(f"SELECT company_name from company_settings").fetchall()[0][0])
st.subheader("Sompany Settings")

#this block doesn't work at all
block_posting = st.toggle("Lock Posting", value=st.session_state.block_posting)


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