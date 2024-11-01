from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pdb



#create a flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key"

# create a form class
class NameForm(FlaskForm):
 name = StringField("What's your name", validators=[DataRequired()])
 submit = SubmitField("Submit")


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

# create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    #debugging
    # pdb.set_trace()  # Sets a breakpoint here

    if request.method == 'POST':
        print("Form submitted:", form.data)
        print("Errors:", form.errors)
    
    # vaidate form
    if form.validate_on_submit():
        name = form.name.data 
        form.name.data = ''
        flash("Form submitted successfully")
    else:
        print("Form submitted but not valid.")
        print("Errors:", form.errors)  # Check what errors are present
        
    return render_template("name.html", name=name, form=form)

if __name__ == '__main__':
    app.run(debug=True)