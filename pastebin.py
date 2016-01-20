from datetime import datetime
from flask import (Flask, request, url_for, redirect, g,
        render_template, session)
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('paste.id'))
    parent = db.relationship('Paste', lazy=True, backref='children',
                             uselist=False, remote_side=[id])

    def __init__(self, user, code, parent=None):
        self.user = user
        self.code = code
        self.pub_date = datetime.utcnow()
        self.parent = parent


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(120))
    fb_id = db.Column(db.String(30), unique=True)
    pastes = db.relationship(Paste, lazy='dynamic', backref='user')


@app.route('/', methods=['GET', 'POST'])
def new_paste():
    parent = None
    reply_to = request.args.get('reply_to', type=int)
    if reply_to is not None:
        parent = Paste.query.get(reply_to)
    if request.method == 'POST' and request.form['code']:
        paste = Paste(g.user, request.form['code'], parent=parent)
        db.session.add(paste)
        db.session.commit()
        return redirect(url_for('show_paste', paste_id=paste.id))
    return render_template('new_paste.html', parent=parent)


@app.route('/<int:paste_id>/')
@app.route('/<int:paste_id>')
def show_paste(paste_id):
    paste = Paste.query.options(db.eagerload('children')).get_or_404(paste_id)
    return render_template('show_paste.html', paste=paste)

