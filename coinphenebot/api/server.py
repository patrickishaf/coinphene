from flask import Flask

server = Flask(__name__)

@server.route("/admin")
def hello():
    return "hello world here"


@server.route("/admin/transactions")
def get_transactions():
    return []


@server.route("/admin/users")
def get_users():
    return [];
