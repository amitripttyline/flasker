from flask import Flask, render_template


#create a flask Instance
app = Flask(__name__)


# create a route decorator
@app.route('/')

# def index():
#     return "<h1>Hello Amit!</h1>"
# '''filters =>
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags
# '''

def index():
    first_name = 'anki'
    stuff = "This is <strong>bold</strong> text"
    color = ['red', 'sky', 55, 'black']
    return render_template('index.html', first_name=first_name, stuff=stuff, color=color)

@app.route("/user/<name>")

def user(name):
    # return "<h1>Hello {}!!!<h1>".format(name)
    return render_template('user.html', user_name= name)


# create custom error pages

#invalid url
@app.errorhandler(404)
def page_not_gound(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_gound(e):
    return render_template("500.html"), 500