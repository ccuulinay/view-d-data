import streamlit as st
import pandas as pd
import requests
import logging
import pathlib
import datetime
import base64
import io
import os

EP_BASE = "http://127.0.0.1:10086"
LOGIN_EP = f"{EP_BASE}/login"
SQL_QUERY_EP = f"{EP_BASE}/query"


RUN_MODE = os.getenv("ST_RUN_MODE", "dev")


def main():
    if 'is_auth' not in st.session_state:
        st.session_state.is_auth = False
    if 'run_result' not in st.session_state:
        st.session_state.run_result = None
    # if "username" not in st.session_state:
    #     st.session_state.username = ""
    # if "password" not in st.session_state:
    #     st.session_state.password = ""

    st.set_page_config(
        page_title="View D data",
        page_icon="",
        layout="wide"
    )
    flow()


def set_header():
    st.title("View D Data")
    st.markdown("""
        - A simple tool to run select statement.
        - Interface for us.
    """)


def transform(df):
    frac = st.slider("Random sample (%)", 1, 100, 100)
    if frac < 100:
        df = df.sample(frac=frac / 100)
    # Select columns to show
    cols = st.multiselect("Columns", df.columns.tolist(), df.columns.tolist())
    rdf = df[cols].copy()
    return rdf


def production_mode():
    # Src: discuss.streamlit.io/t/how-do-i-hide-remove-the-menu-in-production/362
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    return


def flow():
    logging.debug("==================== Flow ===================")
    logging.debug(f"==================== Flow - is_auth: {st.session_state.is_auth} ===================")
    if st.session_state.is_auth:
        authorised_page()
    else:
        login_page()


def authorised_page(run_mode=RUN_MODE):
    logging.debug("==================== main ===================")
    if run_mode != "dev":
        production_mode()
    empty_sb = st.sidebar.empty()
    set_header()
    # st.write("Welcome.")
    with st.form(key="run_sql_form"):
        sql_statement = st.text_area("SQL to run", "", key=f"input_sql_statement")
        sql_run_query = st.form_submit_button(label="Login🦈", on_click=cb_run_sql)

    if isinstance(st.session_state.run_result, pd.DataFrame):
        st.subheader("Result: ")
        df = st.session_state.run_result
        st.write(transform(df))


def cb_run_sql():
    input_sql = {
        "sql": st.session_state.input_sql_statement
    }

    try:
        res = requests.post(SQL_QUERY_EP, json=input_sql)
        if res.status_code == 200:
            r = res.json()
            data = r.get("data")
            cols = r.get("columns")
            df = pd.DataFrame(data, columns=cols)
            st.session_state.run_result = df
        else:
            logging.error("Call api failed")
            pass
    except Exception as e:
        logging.error(e)


def cb_update_sess_state__is_auth():
    cred = {
        "username": st.session_state.sess_username,
        "password": st.session_state.sess_password
    }

    try:
        res = requests.post(LOGIN_EP, json=cred)
        if res.status_code == 200:
            r = res.json()
            st.session_state.is_auth = True
        else:
            st.write("Login failed.")
            st.session_state.is_auth = False
    except Exception as e:
        logging.error(e)
        st.write("Login failed with error.")
        st.session_state.is_auth = False


def login_page(run_mode=RUN_MODE):
    logging.debug("==================== login ===================")
    if run_mode != "dev":
        production_mode()
    # st.session_state.is_auth = False
    set_header()

    with st.form(key="Login_form"):
        with st.sidebar:
            st.subheader(f"Login with username/password")

            username = st.text_input(
                "Username", value="", key="sess_username"
            )

            password = st.text_input(
                "Password", value="", type="password", key='sess_password'
            )

            submitted = st.form_submit_button(label="Login🦈", on_click=cb_update_sess_state__is_auth)

            # cred = {
            #     "username": username,
            #     "password": password
            # }
            #
            # if submitted:
            #     try:
            #         res = requests.post(LOGIN_EP, json=cred)
            #         if res.status_code == 200:
            #             r = res.json()
            #             st.session_state.is_auth = True
            #         else:
            #             st.write("Login failed.")
            #             st.session_state.is_auth = False
            #     except Exception as e:
            #         logging.error(e)
            #         st.write("Login failed with error.")
            #         st.session_state.is_auth = False


if __name__ == "__main__":
    main()
