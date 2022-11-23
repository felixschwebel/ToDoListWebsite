from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

with app.app_context():
    # Connect to Database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Manage Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Table Configuration
    class User(db.Model, UserMixin):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        # Relationships
        lists = relationship("ToDoLists", back_populates="owner")
        tasks = relationship("Tasks", back_populates="owner")

    class ToDoLists(db.Model):
        __tablename__ = "todolists"
        id = db.Column(db.Integer, primary_key=True)
        list_title = db.Column(db.String(250), unique=True, nullable=False)
        # Relationships
        owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        owner = relationship("User", back_populates="lists")
        tasks = relationship("Tasks", back_populates="list")

    class Tasks(db.Model):
        __tablename__ = "tasks"
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(250), nullable=False)
        # Relationships
        owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"))
        list = relationship("ToDoLists", back_populates="tasks")
        owner = relationship("User", back_populates="tasks")

    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(password=password, pwhash=user.password):
                login_user(user)
                return redirect(url_for('all_lists'))
            else:
                flash("Password incorrect. Please try again!")
                return redirect(url_for("login"))
        else:
            flash("That user does not exist. Please try again or sign up.")
            return redirect(url_for("login"))
    return render_template('login.html', form=login_form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    register_form = LoginForm()
    return render_template('register.html', form=register_form)


@app.route('/list')
@login_required
def todo_list():
    return render_template('list.html')


@app.route('/alllists')
@login_required
def all_lists():
    return render_template('all_lists.html')


@app.route('/newlist')
def new_list():
    return render_template('new_list.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)