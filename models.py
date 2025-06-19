from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()

#------------------------Define models----------------------

#------------------------Post model-------------------------
from datetime import datetime
from sqlalchemy.orm import validates

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))            
    body = db.Column(db.Text)                
    image_url = db.Column(db.String(250))         
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #--------------------Handle post validations-----------------
    @validates('title')
    def validate_title(self, key, title):
        if len(title) < 5:
            raise ValueError("Title must be at least 5 characters long.")
        return title

    @validates('body')
    def validate_body(self, key, body):
        if len(body) < 10:
            raise ValueError('Body must be at least 10 characters long.')
        return body
    
    #serialize post
    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'body' : self.body,
            'image_url' : self.image_url,
            'date_created' : self.date_created.isoformat()  
        }
    
    def __repr__(self):
        return f'< Title: {self.title}, Body: {self.body}>'
