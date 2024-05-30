import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_extras.badges import badge
from streamlit_extras.bottom_container import bottom

st.set_page_config(
    page_title="Settings",
    page_icon="🔧",
)


block_posting = st.toggle("Lock Posting", value=False)

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