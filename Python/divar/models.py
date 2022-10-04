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



# class Bookmark(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="cascade"))
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

user_bookmarks = db.Table("user_bookmarks",
    db.Column("users_id",db.Integer, db.ForeignKey("users.id", ondelete="cascade")),
    db.Column("posts_id",db.Integer, db.ForeignKey("posts.id", ondelete="cascade"))
)

class User(db.Model):
    """
    This Table carries all user information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),nullable=True)
    # if you are using a hash generator that create more than 128 character 
    # change password field
    password = db.Column(db.String(128),nullable=False)
    phone = db.Column(db.String(11),nullable=True)
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
    histories = db.relationship("History", backref="user_history", lazy=True)
    notes = db.relationship("Note", backref="user_notes", lazy=True)
    VisitHistories = db.relationship("VisitHistory", backref="user_VisitHistory", lazy=True) 
    
    bookmarks = db.relationship("Post", secondary=user_bookmarks, backref='user_bookmark', lazy=True)



class Post(db.Model):
    """
    This table carries all Post in web site 
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(128))
    post_caption = db.Column(db.String(256))
    # each post has to be have 1 picture at least
    image_location = db.Column(db.Text())
    # in this app we have price and some time (توافقی / حدودی )
    post_price = db.Column(db.String(256),nullable=False)
    # post <sell> or post <is available>
    post_status = db.Column(db.String(64))
    last_date = db.Column(db.DateTime(),default=datetime.utcnow)
    # when we created post assign value to this field
    created_date = db.Column(db.DateTime())
    post_categories = db.Column(db.String(256))
    chat_available = db.Column(db.Boolean(),default=False, nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    notes = db.relationship("Note", backref="post_notes", lazy=True)
    histories = db.relationship("History", backref="post_hostories", lazy=True) 
    VisitHistories = db.relationship("VisitHistory", backref="post_VisitHistory", lazy=True) 
    

class Note(db.Model):
    """
    This Table carries all users note in posts
    """
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(256))

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class History(db.Model):
    """
    This table is log for all users 
    """
    __tablename__ = 'Histories'
    id = db.Column(db.Integer, primary_key=True)
    last_visit = db.Column(db.Date(),default=datetime.utcnow)


    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Category(db.Model):
    """
    This table carries all categories in website
    added automatically via add_CategoryDB.py script
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128), unique=True,nullable=False)


class VisitHistory(db.Model):
    """
    This table carries all user visit posts log
    """
    __tablename__ = 'visit-history'
    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.Date(),default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class State(db.Model):
    """
    This Table carries all States name
    """
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(64), unique=True, nullable=False)
    
    cities = db.relationship("City", backref="state_Cities", lazy=True)

class City(db.Model):
    """
    This Table carries all cities and states id
    """
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64), unique=True, nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))    
    posts = db.relationship("Post", backref="post_cities", lazy=True)

db.create_all()
