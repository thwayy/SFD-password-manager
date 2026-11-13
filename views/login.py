import streamlit as st
from core.auth import login
# login screen
def login_page():
        st.title("Login")
        password = st.text_input("Master password", type="password")

        if st.button("Login"):
                try:
                        key, vault = login(password)
                        st.session_state.key = key
                        st.session_state.vault = vault
                        st.session_state.page="vault"
                        st.rerun()
                except ValueError as error:
                        st.error(str(error))

        # switch to register screen
        if st.button("Don't have an account?", type="tertiary"):
                st.session_state.page="register"
                st.rerun()
