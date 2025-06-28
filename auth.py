import streamlit as st

def check_auth():
    USERNAME = st.secrets["auth"]["username"]
    PASSWORD = st.secrets["auth"]["password"]

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        with st.form("Login"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if user == USERNAME and pwd == PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        st.stop()
