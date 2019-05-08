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

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_blog = Blog(blog_title, blog_body)

        db.session.add(new_blog)
        db.session.commit()

        blog_title_error = ""
        blog_body_error = ""

        if not blog_title:
            blog_title_error = "I need a title."
        if not blog_body:
            blog_body_error = "Where the post at?"
        if blog_title_error or blog_body_error:
            return redirect('/newpost.html', blog_body=blog_body, blog_body_error=blog_body_error, blog_title=blog_title, blog_title_error=blog_title_error)

    blogs = Blog.query.all()

    return render_template('newpost.html', title="Add Blog Entry", blogs=blogs)


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()

    return render_template('blog.html', title="Build A Blog", blogs=blogs)


@app.route('/delete-blog', methods=['POST', 'GET'])
def delete_blogs():

    blog_id = int(request.form['blog-id'])
    blogs = Blog.query.get(blog_id)
    db.session.delete(blogs)
    db.session.commit()

    return redirect('/blog')

if __name__ == '__main__':
    app.run()