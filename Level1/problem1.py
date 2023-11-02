from flask import Flask
from markupsafe import escape
app = Flask(__name__)

@app.route("/")
def Welcome():
    return "Welcome to Flask Web App"


@app.route("/greet/<username>")
def Greet(username):
    return "Hello, {}".format(escape(username))


@app.route('/farewell/<username>')
def projects(username):
    return f"Goodbye, {username}!"


if __name__ == '__main__':
    app.run()