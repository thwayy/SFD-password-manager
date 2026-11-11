import streamlit as st
from core.storage import load_vault
# login screen
def login_page():
        st.title("Login")
        st.text_input("Master password", type="password")

        if st.button("Login"):
                st.session_state.vault = load_vault()
                st.session_state.page="vault"
                st.rerun()

        # switch to register screen
        if st.button("Don't have an account?", type="tertiary"):
                st.session_state.page="register"
                st.rerun()
