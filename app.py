from flask import Flask, redirect, url_for, flash
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cto154@localhost:3306/books'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='tH!$isMy$3crEteK3y!'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75))
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    is_admin = db.Column(db.String(50), default=False)


class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    zip = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.zip = pin


@app.route('/home', methods=["GET", "POST"])
def hello_world():
    if request.form:
        user = User(request.form['email'], request.form['username'], request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('New File Recorded')
    return render_template('home.html')


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


if __name__ == '__main__':
    app.run(debug=True)
