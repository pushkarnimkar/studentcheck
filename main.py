from flask import Flask, render_template
from model import Model
import os
import json

app_dir = os.path.dirname(__file__)
static_path = os.path.join(app_dir, 'static')
print(static_path)
app = Flask(__name__, static_url_path='/static', static_folder=static_path)


@app.route("/dummy_query")
def homepage():
    both = model.query_scores(grade='Grade 3, Maths', ids=list('123456789'))
    return both.to_json()
    # return render_template("page.html", title="HOME PAGE")


@app.route("/dummy_data")
def dummy_data():
    return json.dumps([
        {'name': 'Pushkar', 'email': 'pushkarnim@gmail.com', 'content': 'Lorem Ipsum'},
        {'name': 'Rajas', 'email': 'hacker-rajas@gmail.com', 'content': 'I am the Hacker!'}
    ])


@app.route("/")
def root():
    return render_template("index.html")


# @app.route("/docs")
# def docs():
#     return render_template("page.html", title="docs page")
#
#
# @app.route("/about")
# def about():
#     return render_template("page.html", title="about page")


if __name__ == "__main__":
    model = Model()
    app.run(debug=True)
