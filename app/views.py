from app import app

from flask import render_template, request, redirect, jsonify, make_response


@app.route("/")
def index():

    print(f"Flask ENV is set to {app.config['ENV']}")

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




# fake database using dictionary
users = {
    'mitsuhiko': {
        "name": "Armin Ronacher",
        "bio": "Creator of the Flask framework",
        "twitter_handle": "@mitsuhuijo"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneuer, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}


# dynamic url with one vairable
@app.route("/profile/<username>")
def profile(username):

    user = None
    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)


# dynamic url with multiple variables
@app.route("/multiple/<a>/<b>/<c>")
def multiple(a, b, c):
    return f"a: {a}, b: {b}, c: {c}"


# json with flask
@app.route("/json", methods=["POST"])
def json():

    if request.is_json:
        req = request.get_json()
        response = {
            "message": "JSON reveived",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)

        return res
    
    else:
        res = make_response(jsonify({"message": "No JSON reveived"}), 400)
        return res
    

# flask and fetch API
@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()
    print(req)

    res = make_response(jsonify(req), 200)

    return res


# query strings
@app.route("/query")
def query():

    if request.args:
        args = request.args

        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())

        return f"(Query) {serialized}", 200
    
    else:

        return "No query recevied", 200





