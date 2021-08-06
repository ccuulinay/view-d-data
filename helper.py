import os
import sys
import logging

CUSTOM_MODULE_PATH = os.path.realpath("/Users/ccuulinay/github_proj/py_public_modules")
sys.path.append(CUSTOM_MODULE_PATH)

from tj_hub.db import mysql_helper

from config import DBConfig


def authenticate(u, p):

    # is_auth, ldap_conn = ldap_service.simple_ldap_auth(u, p)
    if u == "teens" and p == "teens":
        return True
    else:
        return False


def get_db_engine():
    global db_engine
    db_engine = mysql_helper.get_tjhub_mysql_engine()
    return db_engine


def get_db_connection():
    global db_connection

    db_user = DBConfig.USER
    db_pass = DBConfig.PASSWORD
    db_host = DBConfig.HOST
    db_name = DBConfig.SCHEMA
    try:
        db_connection = mysql_helper.get_mysql_connection(db_host, db_name, db_user, db_pass)
        if db_connection is not None:
            return db_connection
        else:
            logging.error("Get connection failed.")
    except Exception as e:
        logging.error("Get connection failed.")
        return


def connect_db():
    if "db_connection" not in globals():
        return get_db_connection()
    # elif not db_connection.is_connected:
    #     return get_db_connection()
    else:
        db_connection.ping(reconnect=True)
        return db_connection


def close_db():
    if db_connection is not None:
        db_connection.close()


def run_sql(sql):
    conn = connect_db()
    df = mysql_helper.execute_sql(conn, sql, upper_columns=False)
    return df
