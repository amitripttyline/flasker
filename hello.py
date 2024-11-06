from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pdb #for debug
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#create a flask Instance
app = Flask(__name__)
# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
#secret key
app.config['SECRET_KEY'] = "my_secret_key"
#initialize the db
db = SQLAlchemy(app)

#create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# create a user form class
class UserForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

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

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name =form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully")
    our_users = Users.query.order_by(Users.date_added) 
    return render_template("add_user.html", form=form, name=name, our_users = our_users)


if __name__ == '__main__':
    app.run(debug=True)