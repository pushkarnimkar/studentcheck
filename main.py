from flask import Flask, render_template, redirect
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
        {'name': 'Pushkar', 'pred_vs_perf_latest_diff': 'pushkarnim@gmail.com', 'test_since_at_risk': 'Lorem Ipsum'},
        {'name': 'Rajas', 'pred_vs_perf_latest_diff': 'hacker-rajas@gmail.com', 'test_since_at_risk': 'I am the Hacker!'}
    ])


@app.route("/index.html")
def root():
    return render_template("index.html")


@app.route("/")
def root_alias():
    return redirect("/index.html")


@app.route("/class1.html")
def class1():
    return render_template("class1.html")


@app.route("/class2.html")
def class2():
    return render_template("class2.html")


@app.route("/class3.html")
def class3():
    return render_template("class3.html")


@app.route("/overview/<class_number>")
def at_risk_drop_down(class_number):
    class_name_dict = {
        '1': 'Grade 3, Maths',
        '2': 'Grade 4, Maths',
        '3': 'Grade 5, Maths'
    }
    class_name = class_name_dict[class_number]
    df_student_list = model.query_students(class_name=class_name) #student db filtered by class
    df_overview = df_student_list[df_student_list['at_risk'] == 1][['name','pred_vs_perf_latest_diff','test_since_at_risk']]
    df_overview.loc[0, :] = '1'
    df_overview.loc[1, :] = '1'
    df_overview.loc[2, :] = '1'
    return df_overview.to_json(orient='records')


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
