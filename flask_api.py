from flask import request, abort, make_response
from flask import Flask
from flask import jsonify
from flask import after_this_request, before_render_template

import random
import logging
import os
import pathlib

import helper


APP_NAME = "VIEW_D_DATA_FLASK_API"

################### Get logger ###################
# set up basic config - logging to console
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s: %(name)s: %(message)s',
                    # datefmt='%m-%d %H:%M',
                    # filename='/temp/myapp.log',
                    # filemode='w'
                    )

# Create console handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
c_handler.setFormatter(c_format)

# Create file handler
log_f_path = os.environ.get("APP_LOG_PATH", os.path.dirname(__file__))
log_f_p = pathlib.Path(log_f_path) / "logs"
log_f_p.mkdir(parents=True, exist_ok=True)
log_f = log_f_p / "app_flask.log"
f_handler = logging.FileHandler(log_f)
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
f_handler.setFormatter(f_format)

# Add hanlder to root logger.
logging.getLogger('').addHandler(f_handler)

# Create a custom logger
logger = logging.getLogger(APP_NAME)

logger.setLevel(logging.INFO)

app = Flask(APP_NAME)


@app.route("/query", methods=["POST"])
def run_query():
    if request.method == "POST":
        data = request.get_json()
        sql = data.get("sql")
        if (sql is not None) and (isinstance(sql, str)):
            if (
                    sql.upper().startswith("INSERT") |
                    sql.upper().startswith("UPDATE") |
                    sql.upper().startswith("DELETE") |
                    sql.upper().startswith("GRANT") |
                    (not sql)
            ):
                r_msg = {
                    "code": 400,
                    "result": "Only SELECT statement is allowed."
                }
                abort(make_response(jsonify(r_msg), 400))
            else:
                df = helper.run_sql(sql)
                data_rows = df.values.tolist()
                data_cols = df.columns.tolist()
                r = {
                    "code": 200,
                    "data": data_rows,
                    "columns": data_cols
                }
                logger.info(f"SQL run successfully.")
                return jsonify(r)
        else:
            logger.error(f"SQL is string.")
            return abort(400)


@app.route("/login", methods=["POST"])
def is_authorized():
    if request.method == "POST":
        data = request.get_json()
        u = data.get("username")
        p = data.get("password")
        if (u is not None) and (p is not None):
            is_auth = helper.authenticate(u, p)
            if is_auth:
                r_msg = {
                    "status_code": 200,
                    "result": f"Welcome {u}"
                }
                return jsonify(r_msg)
            else:
                r_msg = {
                    "code": 401,
                    "result": "Please confirm your username/password and you have proper access to the tool."
                }
                abort(make_response(jsonify(r_msg), 400))
        else:
            abort(400)


@app.route("/ping", methods=['GET'])
def pong():
    pop = ["pong", "oop!"]
    r = random.choices(population=pop, weights=[0.8, 0.2], k=1)
    return r[0]


@app.route("/")
def index():
    return "你好"


@app.route('/mirror_parse', methods=['GET', 'POST'])
def mirror_parse():
    if request.method == 'POST':
        return post_call(request)
    elif request.method == 'GET':
        return get_call(request)


def post_call(req):
    data = req.get_json()
    print(data)
    return jsonify(data)


def get_call(req):
    args = req.args
    print(args)
    return str(args)


@app.before_request
def before_request_func():
    logger.info("before_request is running!")


@app.after_request
def after_request_func(response):
    msg = {
        "app_name": APP_NAME,
        "req_method": request.method,
        "req_json_data": request.get_json(),
        "req_args": request.args,
        "res_status_code": response.status_code,
        "resp_data": response.get_data(),
        "res_json_data": response.get_json(),
    }
    logger.debug(f"AFTER REQUEST: {msg}")
    # paint_color_helper.save_paint_color_api_audit_log(msg)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10086, debug=True, threaded=True, )