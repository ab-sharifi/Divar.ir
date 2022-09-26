from datetime import datetime
from divar import db


class MailVerification(db.Model):
    """
    This table is for validate user email and identity
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    send_time = db.Column(db.DateTime(),nullable=False)
    exp_time = db.Column(db.DateTime(),nullable=False)
    active_code = db.Column(db.Integer, nullable=True)
    # 0 not active || 1 activated
    activated = db.Column(db.Integer,default=0)
    

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class User(db.Model):
    """
    This Table carries all user information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),nullable=True)
    # if you are using a hash generator that create more than 128 character 
    # change password field
    password = db.Column(db.String(128),nullable=True)
    phone = db.Column(db.Integer, unique=True,nullable=True)
    # in this app login is via email of user so email should be unique here
    email = db.Column(db.String(256),unique=True,nullable=False)
    create_time = db.Column(db.Date(),default=datetime.utcnow)
    # 0 = account not activated 
    # 1 = account activated
    is_active = db.Column(db.Integer, default=0)
    state_id = db.Column(db.Integer,nullable=True)
    profile_image = db.Column(db.String(95),nullable=False, default="default.jpg")
    

    mails = db.relationship("MailVerification", backref="user_mails", lazy=True)
    posts = db.relationship("Post", backref="user_posts", lazy=True)

class Post(db.Model):
    """
    This table carries all Post in web site 
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(32))
    post_caption = db.Column(db.String(256))
    # each post has to be have 1 picture at least
    image_location = db.Column(db.String(256))
    # in this app we have price and some time (توافقی / حدودی )
    post_price = db.Column(db.String(256),nullable=False)
    # post <sell> or post <is available>
    post_status = db.Column(db.String(64))
    last_date = db.Column(db.DateTime(),default=datetime.utcnow)
    # when we created post assign value to this field
    created_date = db.Column(db.DateTime())
    post_categories=db.Column(db.String(256))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Note(db.Model):
    """
    This Table carries all users note in posts
    """
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)


class History(db.Model):
    """
    This table is log for all users 
    """
    __tablename__ = 'Histories'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    last_visit = db.Column(db.Date(),default=datetime.utcnow)


class Category(db.Model):
    """
    This table carries all categories in website
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)


class VisitHistory(db.Model):
    """
    This table carries all user visit posts log
    """
    __tablename__ = 'visit-history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    visit_date = db.Column(db.Date(),default=datetime.utcnow)


class State(db.Model):
    """
    This Table carries all States name
    """
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(64))


class City(db.Model):
    """
    This Table carries all cities and states id
    """
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64))
    state_id = db.Column(db.Integer)

db.create_all()
