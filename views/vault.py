import streamlit as st
from core.auth import save_vault, delete_all
from core.vault_actions import add_entry, edit_entry, delete_entry
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
    
    #load vault decrypted by key    
    entries = st.session_state.vault["entries"]
    if not entries:
        st.info("Your vault is empty. Click Add to save your first password.")
    # header row of table
    col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 1, 1])
    col1.markdown("**Username**")
    col2.markdown("**Password**")
    col3.markdown("**Website**")  

    for entry in entries:
        col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 1, 1], vertical_alignment="center")
        col1.text(entry["username"])    
        col2.text(entry["password"])
        col3.text(entry["website"]) 
        if col4.button("", icon=":material/edit:", type="tertiary",
                       key="edit_" + entry["id"], help="Edit"):
            edit_dialog(entry)
        if col5.button("", icon=":material/delete:", type="tertiary",
                       key="delete_" + entry["id"], help="Delete"):
            delete_dialog(entry)
### pop-up modals
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

@st.dialog("Edit entry")
def edit_dialog(entry):
    with st.form("edit_form"):
        # boxes start filled in with the current values
        website=st.text_input("Website (url)", value=entry["website"], placeholder="optional")
        username=st.text_input("Username", value=entry["username"], placeholder="optional")
        password=st.text_input("Password*", value=entry["password"], type="password", placeholder="required")
        submitted = st.form_submit_button("Save changes")
        if submitted:
            if not password:
                        st.error("Password is required.")
                        return
            edit_entry(st.session_state.vault, entry["id"], username, password, website)
            save_vault(st.session_state.vault, st.session_state.key)
            st.rerun() #close modal and show the change

@st.dialog("Delete entry")
def delete_dialog(entry):
    st.write("Deleting this entry? This cannot be undone")
    if st.button("Delete", key="confirm_delete_entry"):
        delete_entry(st.session_state.vault, entry["id"])
        save_vault(st.session_state.vault, st.session_state.key)
        st.rerun() #close modal and show the change