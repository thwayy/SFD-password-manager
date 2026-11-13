import streamlit as st
from core.auth import save_vault, delete_all
from core.vault_actions import add_entry
from views.generator_view import display_generator

def vault_page():
# go back to login if there is no key in memory
    if "key" not in st.session_state:
        st.session_state.page = "login"
        st.rerun()

    title_col, icon_col = st.columns([9, 1], vertical_alignment="center")
    with title_col:
        st.title("This is your vault.")
    with icon_col:
        if st.button("", icon=":material/delete:", type="tertiary",
                     key="delete_vault", help="Delete vault"):
            delete_vault_dialog()
    st.write("Your saved passwords will appear here.")
    
    # button to go to password generator
    if st.button("Generate a password", icon=":material/autorenew:"):
        display_generator()  
    # button to lock vault
    if st.button("Lock vault", icon=":material/lock:"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()

    #button to add an entry
    if st.button("Add", icon=":material/add:"):
        add_dialog()
        
   
    entries = st.session_state.vault["entries"] #get the entries dictionary from load vault
    st.dataframe(entries, column_config={"id": None})

@st.dialog("Add entry",position="center") #dialog function decorator
def add_dialog():
    with st.form("add_form"):
        website=st.text_input("Website (url)", placeholder="optional")
        username=st.text_input("Username", placeholder="optional")
        password=st.text_input("Password*",type="password", placeholder="required")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not password:
                        st.error("Password is required.")
                        return
            add_entry(st.session_state.vault, username, password, website )
            save_vault(st.session_state.vault, st.session_state.key)
            st.rerun() #close modal and show new entry

@st.dialog("Delete vault")
def delete_vault_dialog():
     st.warning("This will delete your master password and all saved passwords. This action cannot be undone.", icon=":material/warning:")
     if st.button("Delete", key="delete_all"):
        delete_all()
        st.session_state.clear()
        st.session_state.page="register"
        st.rerun()
