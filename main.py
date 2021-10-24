from flask import Flask, render_template
from model import Model

app = Flask(__name__)
model = Model()


@app.route("/")
def homepage():
    both = model.query_scores(grade='Grade 3, Maths', ids=list('123456789'))
    return both.to_json()
    # return render_template("page.html", title="HOME PAGE")


# @app.route("/docs")
# def docs():
#     return render_template("page.html", title="docs page")
#
#
# @app.route("/about")
# def about():
#     return render_template("page.html", title="about page")


if __name__ == "__main__":
    app.run(debug=True)
