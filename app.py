from app import app, db
from app.models import User, Post

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cto154@localhost:3306/books'
#app.config['SQLALCHEMY_ECHO'] = True
#db = SQLAlchemy(app)
#app.secret_key='tH!$isMy$3crEteK3y!'


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post }



