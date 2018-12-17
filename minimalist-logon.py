from flask import Flask, url_for, render_template, session, redirect, request

app = Flask(__name__)


@app.route("/")
def index():
	return "this is an index"


if __name__ == "__main__":
	app.config["ENV"] = "development"
	app.run("127.0.0.1", "5000", debug=True)
