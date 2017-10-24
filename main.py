from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blog-User:trump@localhost:8889/build-a-blog'
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(254))
    body = db.Column(db.String(2000))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET'])
def index():    
    blogs = Blog.query.all()       
    
    if request.args:
        blog_id = request.args.get('id')
        blog_post = Blog.query.get(blog_id)
        return render_template('blog_posts.html', blog=blog_post) 

    return render_template("index.html", blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def enter_blog():
    
    
    if request.method == 'POST':
        title_entry = request.form['title']
        body_entry = request.form['body']
                
        
        if len(title_entry) == 0:             
            flash('You must have a title for your blog.', 'error')

        if len(body_entry) == 0:
            flash('You must have an entry for your blog.', 'error')        
        
        if len(title_entry) > 0 and len(body_entry) > 0:
            new_blog = Blog(title_entry, body_entry)
            db.session.add(new_blog)
            db.session.commit()
            db.session.refresh(new_blog)           
            return redirect('/blog?id='+ str(new_blog.id))

        return render_template('add-entry.html', entry_title=title_entry, entry_body=body_entry)
    

    return render_template('add-entry.html')


if __name__ == '__main__':
    app.run()