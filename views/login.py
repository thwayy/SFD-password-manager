import streamlit as st
from core.auth import login
MAX_LOGIN_ATTEMPTS = 3

# login screen
def login_page():
        st.title("Login")
        with st.form("register_form"):
                password = st.text_input("Master password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
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
