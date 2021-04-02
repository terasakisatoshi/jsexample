from flask import Flask
from flask import request, render_template

app = Flask(__name__)


@app.route('/', methods=["POST"])
def form():
    ck = request.form.get("check")
    rd = request.form.get("radio")
    sel = request.form.getlist("sel")
    return render_template(
        "index.html",
        title="Contorls",
        message=[ck, rd, sel],
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Title", message="Hi")


if __name__ == "__main__":
    app.run()
