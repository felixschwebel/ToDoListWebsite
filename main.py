from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/alllists')
def all_lists():
    return render_template('all_lists.html')


@app.route('/newlist')
def new_list():
    return render_template('new_list.html')


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)