from app import app

from flask import render_template, request, redirect


@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/jinja")
def jinja():

    project_name = "Machine Learning Dashboard"

    langs = ['Python', 'C++', 'Java', "Ruby", "Go"]

    colors = ("Green", "Red")


    def multiply(x, times):
        return x * times


    return render_template("public/jinja.html", project_name=project_name,
                            langs=langs, colors=colors, multiply=multiply)


@app.route("/about")
def about():
    return "I'm in about!"


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        req = request.form
        
        username = req['username']
        email = req.get('email')
        password = request.form['password']
        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sign_up.html")