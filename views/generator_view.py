import streamlit as st
# from core.password_generator import generate_password 
def display_generator():
    st.title("Password generator")
    # create slider element and store password length value
    length = st.slider("Length", min_value=4, max_value=64, value=8)
    # create checkboxes for password generation parameters
    use_upper = st.checkbox("Uppercase (A-Z)", value=True)   
    use_lower = st.checkbox("Lowercase (a-z)", value=True)
    use_numbers = st.checkbox("Numbers (0-9)", value=True)
    use_special = st.checkbox("Special characters (!@#$...)", value=True)
    st.button("Generate new password")
    # must check at least one box
    if not (use_upper or use_lower or use_numbers or use_special):
        st.warning("Pick at least one character type.")
        return None

    st.code("placeholder")
