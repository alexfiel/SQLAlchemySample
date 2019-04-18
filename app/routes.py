from flask import render_template, flash, redirect, request
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


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
