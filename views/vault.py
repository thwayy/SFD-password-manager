import json
import streamlit as st

def vault_page():
    st.title("This is your vault.")
    st.write("Your saved passwords will appear here.")
    with open("vault.json", "r") as file:
        vault = json.load(file)
    st.dataframe(vault["entries"])