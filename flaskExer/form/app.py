from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title="Form Sample",
        message="What is your name?",
    )


@app.route("/", methods=["POST"])
def form():
    field = request.form["field"]
    return render_template(
        "index.html",
        title="Form Sample",
        message="Hi %s" % field
    )


@app.route("/<user>/<message>", methods=["GET"])
def index2(user, message):
    return render_template("index.html", title="title", message=f"{user} sent {message}")


def main():
    app.debug = True
    app.run(host="localhost")


if __name__ == '__main__':
    main()
