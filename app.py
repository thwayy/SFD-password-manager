import streamlit as st

# login screen
def login_page():
        st.title("Login")
        st.text_input("Master password")
        st.button("Login")
        # switch to register screen
        if st.button("Don't have an account?", type="tertiary"):
                st.session_state.page="register"
                st.rerun()

# register screen
def register_page():
        st.title("Register")
        st.text_input("Create Master Password")
        st.text_input("Confirm Master Password")
        st.button("Register")
        # switch to login screen
        if st.button("Already have an account?", type="tertiary"):
                st.session_state.page="login"
                st.rerun()
                
# show login screen at startup
if "page" not in st.session_state:
    st.session_state.page = "login"  
#call function based on session state  
if st.session_state.page=="login":
        login_page()
elif st.session_state.page=="register":
        register_page()



