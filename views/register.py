import streamlit as st
from core.auth import register
# register screen
def register_page():
        st.title("Register")
        with st.form("register_form"):
                password = st.text_input("Create Master Password", type="password")
                confirm = st.text_input("Confirm Master Password", type="password")
                submitted = st.form_submit_button("Register")
                if submitted: 
                        try:
                                key, vault = register(password, confirm)
                                st.session_state.key = key
                                st.session_state.vault = vault
                                st.session_state.page="vault"
                                st.rerun()
                        except ValueError as error:
                                st.error(str(error))
        # switch to login screen
        if st.button("Already have an account?", type="tertiary"):
                st.session_state.page="login"
                st.rerun()
