from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi
from models import User, Blog
from hashutils import check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:centauri@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'c337kGcys&zP3B'



@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')


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