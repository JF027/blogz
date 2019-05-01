from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:centauri@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'c337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    return render_template('newpost.html', title="Add Blog Entry")


@app.route('/blog', methods=['POST', 'GET'])
def blog():


    if request.method == 'POST':
        blog_title = request.form['blog-title']
        new_post = Blog(blog_title)
        db.session.add(new_post)
        db.session.commit()

    
    return render_template('blog.html', title="Build A Blog")

if __name__ == '__main__':
    app.run()