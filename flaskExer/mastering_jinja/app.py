from flask import Flask
from flask import request, render_template
app = Flask(__name__)


@app.route('/', methods=["POST"])
def post():
    numberlike = request.form.get("number")
    warning = True
    if numberlike.isnumeric():
        number = float(numberlike)
        if number.is_integer() and (int(number) % 2 == 0):
            warning = False
    return render_template(
        "index.html",
        title="Title",
        message="This is a Jinja template sample",
        warning=warning,
        data=["A", "B", "C"],
    )


@app.route('/', methods=["GET"])
def index():
    warning = True
    return render_template(
        "index.html",
        title="Title",
        message="This is a Jinja template sample",
        warning=warning,
        data=["A", "B", "C"],
    )


if __name__ == "__main__":
    app.run(debug=True)
