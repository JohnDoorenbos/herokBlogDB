#Many Tags to many Posts

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route("/initdb")

def initDB():

    post_tags = db.Table('post_tags',
                         db.Column('title',db.Text, db.ForeignKey('post.title')),
                         db.Column('name',db.Text, db.ForeignKey('tag.name'))
                     )
    class Post(db.Model):
        __tablename__ = "post"
        title = db.Column(db.Text, primary_key = True)
        author = db.Column(db.Text)
        text = db.Column(db.Text)
        tags = db.relationship('Tag',secondary = post_tags, backref= db.backref('posts',lazy='dynamic'))
        
    class Tag(db.Model):
        __tablename__ = "tag"
        name = db.Column(db.Text, primary_key = True)
        firstDate = db.Column(db.DateTime)
        desc = db.Column(db.Text)
            
    db.drop_all()
    db.create_all()
    t1 = Tag(name = "foo",firstDate= datetime.datetime.now(),desc = "This is a tag for Foo")
    t2 = Tag(name = "bar", firstDate = datetime.datetime.now(), desc = "This is a tag for Bar")
    
    db.session.add_all([t1,t2])
    
    p1 = Post(title = "Hello World", author = "John", text = "Nothing here at all!", tags = [t1,t2])
    p2 = Post(title = "Trix are Tasty", author = "Karl", text = "HAAAANNNDDDSSSS!", tags = [t1])
    
    db.session.add_all([p1,p2])
    
    db.session.commit()
    
    return "Database Created"


if __name__ == "__main__":
    app.run(debug=True)


#link on katie. walk through enabling postgres
