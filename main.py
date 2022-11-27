from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from flask_ckeditor import CKEditor, CKEditorField


def extract_tasks(data):
    return [item.strip() for item in data.split(",")]


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class ToDoListForm(FlaskForm):
    list_title = StringField(label='Title', validators=[DataRequired()])
    body = CKEditorField(label='Body')
    submit = SubmitField(label='submit')


app = Flask(__name__)
bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)
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
        checked = db.Column(db.Boolean)
        # Relationships
        owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        owner = relationship("User", back_populates="tasks")
        list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"))
        list = relationship("ToDoLists", back_populates="tasks")


    db.create_all()


@app.route('/')
def home():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(password=password, pwhash=user.password):
                    login_user(user)
                    return redirect(url_for('all_lists', owner_id=current_user.id))
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
    if request.method == "POST":
        if User.query.filter_by(email=register_form.email.data).first() is not None:
            flash("You have an account already, please login instead!")
            return redirect(url_for("login"))
        else:
            new_user = User()
            new_user.email = register_form.email.data
            new_user.password = generate_password_hash(password=register_form.password.data,
                                                       method='pbkdf2:sha256', salt_length=8)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('all_lists', owner_id=current_user.id))
    return render_template('register.html', form=register_form)


@app.route('/list/<int:list_id>', methods=['POST', 'GET'])
@login_required
def todo_list(list_id):
    title = ToDoLists.query.get(list_id).list_title
    todos = db.session.execute(db.select(Tasks).filter_by(list_id=list_id).order_by(asc(Tasks.checked))).scalars()
    if request.method == 'POST':
        response = [int(i[0]) for i in request.values.lists()]
        for index in todos:
            if index.id in response:
                task_to_update = Tasks.query.get(index.id)
                task_to_update.checked = 1
            else:
                task_to_update = Tasks.query.get(index.id)
                task_to_update.checked = 0
            db.session.commit()
        return redirect(url_for('todo_list', list_id=list_id))
    return render_template('list.html', title=title, todos=todos, list_id=list_id)


@app.route('/alllists/<int:owner_id>')
@login_required
def all_lists(owner_id):
    any_item = ToDoLists.query.filter_by(owner_id=owner_id).first()
    if any_item is None:
        items = 0
    else:
        items = 10
    all_todolists = db.session.execute(db.select(ToDoLists).filter_by(owner_id=owner_id)).scalars()

    return render_template('all_lists.html', todolists=all_todolists, items=items)


@app.route('/newlist', methods=['POST', 'GET'])
@login_required
def new_list():
    user_form = ToDoListForm()
    if request.method == 'POST':
        if user_form.validate_on_submit():
            new_todolist = ToDoLists(
                list_title=user_form.list_title.data,
                owner_id=current_user.id,
            )
            db.session.add(new_todolist)
            db.session.commit()

            data = user_form.body.data.strip('<p>').replace('</p>', "").replace('&nbsp', "").strip()
            todos = extract_tasks(data)
            for task in todos:
                new_tasks = Tasks(
                    text=task,
                    owner_id=current_user.id,
                    list_id=ToDoLists.query.filter_by(list_title=user_form.list_title.data).first().id
                )
                db.session.add(new_tasks)
                db.session.commit()
            return redirect(url_for('todo_list', list_id=ToDoLists.query.filter_by(list_title=user_form.list_title.data).first().id))
    return render_template('new_list.html', form=user_form)


@app.route('/edit/<int:list_id>', methods=['POST', 'GET'])
@login_required
def edit_list(list_id):
    title = ToDoLists.query.get(list_id).list_title
    todos = db.session.execute(db.select(Tasks).filter_by(list_id=list_id).order_by(asc(Tasks.checked))).scalars()

    if request.method == 'POST':
        response = request.values.lists()
        for item in response:
            if item[0] == 'title':
                list_to_change = ToDoLists.query.get(list_id)
                list_to_change.list_title = item[1][0]
            else:
                task = Tasks.query.get(int(item[0]))
                task.text = item[1][0]
            db.session.commit()
        return redirect(url_for('todo_list', list_id=list_id))
    return render_template('edit_list.html', title=title, todos=todos, list_id=list_id)


@app.route('/addtask/<int:list_id>')
@login_required
def add_task(list_id):
    new_task = Tasks(text="", list_id=list_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('edit_list', list_id=list_id))


@app.route('/deletetask/<int:task_id>, <int:list_id>')
@login_required
def delete_task(task_id, list_id):
    task_to_delete = Tasks.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('edit_list', list_id=list_id))


@app.route('/delete/<int:list_id>')
@login_required
def delete_list(list_id):
    list_to_delete = ToDoLists.query.get(list_id)
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for('all_lists', owner_id=current_user.id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)