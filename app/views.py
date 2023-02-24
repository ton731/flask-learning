from app import app

from flask import render_template, request, redirect, jsonify, make_response

import os

from werkzeug.utils import secure_filename


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
# @app.route("/profile/<username>")
# def profile(username):

#     user = None
#     if username in users:
#         user = users[username]

#     return render_template("public/profile.html", username=username, user=user)


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



app.config["IMAGE_UPLOADS"] = "app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_image(filename):
    if "." not in filename:
        return False
    
    extension = filename.split(".")[-1]
    if extension.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    return False


# uploading files with flask
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:

            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("File exceed maximum size")
                return redirect(request.url)

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extensions is not allowed")
                return redirect(request.url)
            
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print(f"Image saved: {filename}")

            return redirect(request.url)

    return render_template("public/upload_image.html")




# sending files
from flask import send_from_directory, abort

# app.config["CLIENT_IMAGES"] = "app/static/client/img"
app.config["CLIENT_IMAGES"] = "/Users/tony/Desktop/flask-learning/app/static/client/img"

@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], 
            path=image_name,
            as_attachment=False)
    
    except FileNotFoundError:
        abort(404)


# flask cookies
@app.route("/cookies")
def cookies():

    res = make_response("Cookies", 200)

    res.set_cookie("flavor", 
                   value="chocolate chip",
                   max_age=10,
                   expires=None,
                   path=request.path,
                   domain=None,
                   secure=False,
                   httponly=False,
                   samesite=False)


    cookies = request.cookies
    flavor = cookies.get("flavor")
    print("cookie flavor:", flavor)

    return res



# Flask session object
from flask import session, url_for

app.config["SECRET_KEY"] = "sdglishgqithqo-rrqhia"

#  a mock database
users = {
    "tony": {
    "username": "tony",
    "email": "tony@gmail.com",
    "password": "tony123",
    "bio": "civil engeering"
    },
    "ivy": {
    "username": "ivy",
    "email": "ivy@gmail.com",
    "password": "ivy123",
    "bio": "anthorpology"
    }
}

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        # this is purely to demonstrate session object
        # don't use these in real production, it's not safe

        if username not in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            print("Password incorrect")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("User added to session")
            return redirect(url_for("profile"))

    return render_template("public/sign_in.html")


@app.route("/profile/")
def profile():

    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", username=username, user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))
    
    
@app.route("sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("sign_in"))

