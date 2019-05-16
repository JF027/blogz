from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi
import re
#from models import User, Blog
#from hashutils import check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:centauri@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'c337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_pw_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("home.html")

@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html")

@app.route("/register", methods=['GET'])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=['POST'])
def register():
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    password2 = cgi.escape(request.form['password2'])
    email = cgi.escape(request.form['email'])

    username_error = ""
    password_error = ""
    password2_error = ""
    email_error = ""

    if not username:
        username_error = "Please enter a username."

    if not password:
        password_error = "Please enter a password."

    elif len(password) < 3:
        password_error = "Password should be between 3 and 20 characters."

    elif len(password) > 20:
        password_error = "Password should be between 3 and 20 characters."
    
    if password2 != password:
        password2_error = "Please match this password with the first one."

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        email_error = "Please enter a valid email."

    if username_error or password_error or password2_error or email_error:
        return render_template("register.html", username=username, usernameError=username_error, password=password, passwordError=password_error, password2=password2, password2Error=password2_error, email=email, emailError=email_error)

    return 'Welcome, ' + username 


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        
        blog_title_error = ""
        blog_body_error = ""

        if blog_title == "":
            blog_title_error = "I need a title."
        if blog_body == "":
            blog_body_error = "Where the post at?"

        if not blog_body_error and not blog_title_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')

        return render_template('newpost.html', blog_body_error=blog_body_error, blog_title_error=blog_title_error, blog_body=blog_body, blog_title=blog_title)
    

    blogs = Blog.query.all()

    return render_template('newpost.html', title="Add Blog Entry", blogs=blogs)


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body)

    return render_template('blog.html', title="Build A Blog", blogs=blogs)


if __name__ == '__main__':
    app.run()