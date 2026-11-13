import streamlit as st
from core.auth import save_vault
from core.vault_actions import add_entry

def vault_page():
# go back to login if there is no key in memory
    if "key" not in st.session_state:
        st.session_state.page = "login"
        st.rerun()    
    st.title("This is your vault.")
    st.write("Your saved passwords will appear here.")
    
    # button to go to password generator
    if st.button("Generate a password"):
        st.session_state.page = "generator"
        st.rerun()   
    # button to lock vault
    if st.button("Lock vault"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()

    #button to add an entry
    if st.button("+ Add"):
        add_dialog()
        
   
    entries = st.session_state.vault["entries"] #get the entries dictionary from load vault
    st.dataframe(entries, column_config={"id": None})

@st.dialog("Add entry",position="center") #dialog function decorator
def add_dialog():
    with st.form("add_form"):
        website=st.text_input("Website(url)")
        username=st.text_input("Username")
        password=st.text_input("Password",type="password")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not password:
                        st.error("Password is required.")
                        return
            add_entry(st.session_state.vault, username, password, website )
            save_vault(st.session_state.vault, st.session_state.key)
            st.rerun() #close modal and show new entry