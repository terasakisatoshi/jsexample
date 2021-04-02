from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template(
        "index.html",
        title="Title",
        message="Hello World",
    )


if __name__ == '__main__':
    app.run(debug=True)
