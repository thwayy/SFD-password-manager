import json
import streamlit as st

def vault_page():
    st.title("This is your vault.")
    st.write("Your saved passwords will appear here.")

    # button to go to password generator
    if st.button("Generate a password"):
        st.session_state.page = "generator"
        st.rerun()   
    # button to lock vault
    if st.button("Lock vault"):
        st.session_state.page = "login"
        st.rerun()


    with open("vault.json", "r") as file:
        vault = json.load(file)

    #button to add an entry
    if st.button("Add"):
        add_dialog()
    # with st.form("my_form"):
    #     st.write("Inside the form")
    #     slider_val = st.slider("Form slider")
    #     checkbox_val = st.checkbox("Form checkbox")

    #     # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")
    #     if submitted:
    #         st.write("slider", slider_val, "checkbox", checkbox_val)
    # st.write("Outside the form")    
    st.data_editor(vault["entries"], disabled=["id"])

@st.dialog("Add entry",position="center") #dialog function decorator
def add_dialog():
    st.markdown("form")