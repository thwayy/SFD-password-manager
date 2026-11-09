import streamlit as st
# register screen
def register_page():
        st.title("Register")
        st.text_input("Create Master Password")
        st.text_input("Confirm Master Password")
        if st.button("Register"):
                st.session_state.page="vault"
                st.rerun()
        # switch to login screen
        if st.button("Already have an account?", type="tertiary"):
                st.session_state.page="login"
                st.rerun()
