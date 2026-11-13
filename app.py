import streamlit as st
from views import login_page, register_page, vault_page
from pathlib import Path

css_path = Path(__file__).parent / "styles" / "style.css"

st.html(css_path)

                
# show login screen at startup
if "page" not in st.session_state:
    st.session_state.page = "login"  
#call screen function based on session state  
if st.session_state.page=="login":
        login_page()
elif st.session_state.page=="register":
        register_page()
elif st.session_state.page=="vault":
        vault_page()




