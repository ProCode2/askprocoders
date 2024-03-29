import os
from flask import Flask, render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length,ValidationError
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user

#initialising flask app
app = Flask(__name__)

#fetching Environment configs from config.py
app.config.from_object("config.ProductionConfig")


Bootstrap(app)

#creating sqlalchemy instance for creating tables in the database 
db = SQLAlchemy(app)

#instance of flask login manager
login_manager = LoginManager()

#Wrapping app with login manager to handle login logouts
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#class to check if every username is unique or not
class Unique(object):
    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


#class to create "users" table in the database
class users(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	answered = db.Column(db.Integer, nullable=True)

#clas to create "qa" table to store question and answer in the database
class qa(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	id = db.Column(db.BigInteger, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	questions = db.Column(db.Text, nullable=False)
	answers = db.Column(db.Text, nullable=True)
	send = db.Column(db.String, nullable=True)


@login_manager.user_loader
def loaduser(user_id):
	return users.query.get(int(user_id))

#Login form back-end workings
class LoginForm(FlaskForm):
	username = StringField('username' , validators = [InputRequired(),Length(min = 4 ,max=16)])
	password = PasswordField('password' , validators = [InputRequired() , Length(min = 6, max = 80)])
	remember = BooleanField('remember me')

# Sign-in or Registration form back-end workings
class RegistrationForm(FlaskForm):
	email = StringField('email' , validators = [InputRequired() , Email('Invalid email') , Length(max = 50) , Unique( users,users.email,message='There is already an account with that email.')])
	username = StringField('username' , validators = [InputRequired(),Length(min = 4 ,max=16) ,  Unique( users,users.username,message=''' Don't you wanna be a bit DIFFERENT from others!  ''')])
	password = PasswordField('password' , validators = [InputRequired() , Length(min = 6, max = 80)])



#Home page view routing/rendering
@app.route('/')
def index():
    return render_template('index.html')

#Login page view
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password </h1><p>Please consider going back and Retry</p>'

    return render_template('login.html', form=form)


#Signup page view
@app.route('/signup', methods = ['GET' , 'POST'])
def signup():
	form = RegistrationForm()
	hashed_password = generate_password_hash(form.password.data , method = 'sha256')
	if form.validate_on_submit():
		new_user = users(username = form.username.data , email = form.email.data , password= hashed_password)
		db.session.add(new_user)
		db.session.commit()
	return render_template('signup.html' , form = form)

#dashboard view
@app.route('/dashboard' , methods = ['GET' , 'POST'])
@login_required
def dashboard():
	searched_posts= []
	posts = qa.query.filter_by(send = None).all()
	if request.method=='POST':
		search = request.form['search']
		for post in posts:
			if search.lower() in post.questions.lower():
				searched_posts.append(post)
	else:
		searched_posts=posts
	return render_template('dashboard.html' , name = current_user.username , posts =searched_posts)

#user logout handler
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

#Answer View
@app.route('/answer/<int:post_id>' , methods = ['GET'])
@login_required
def answer(post_id):
	post = qa.query.filter_by(sno = post_id).first()
	return render_template('answer.html' , post = post)


#storing answer in the database
#answer page view
@app.route('/submit' , methods = ['POST'])
@login_required
def answ():
	global qa
	answ = request.form['ans']
	id = request.form['id']
	user_update = users.query.filter_by(username = current_user.username).first()
	if user_update.answered  ==None:
		user_update.answered=0
	user_update.answered +=1;
	db.session.commit()
	qa=qa.query.filter_by(id = id).first()
	qa.answers=answ
	db.session.commit()
	return render_template('submit.html' , ans = answ , id = id)

#404 not found error handler
@app.errorhandler(404)
def not_found(e):
	return render_template('404.html')

#main function
#app runner
#creating all databases
if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(
    	host="0.0.0.0",
        port=port,
    )

