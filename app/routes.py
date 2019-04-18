from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from app.models import User
from app import db
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    user ={'username': 'Alex'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'New Awesome!'
        },
        {
            'author': {'username': 'Peter'},
            'body': 'Picture perfect!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/home', methods=["GET", "POST"])
def hello_world():
    if request.form:
        user = User(request.form['email'], request.form['username'], request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('New File Recorded')
    return render_template('home.html')


@app.route('/view')
def view_all():
    return render_template('view_all.html', Students = Students.query.all() )


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('view_all'))
    return render_template('new.html')
