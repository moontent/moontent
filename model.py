
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from datetime import datetime

engine = create_engine("sqlite:///moontent.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

following_table = Table('following', Base.metadata,
    Column('follower', Integer, ForeignKey('users.id')),
    Column('followed', Integer, ForeignKey('users.id')))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    # TODO: enforce uniqueness on username
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime())

    following = relationship("User", 
        secondary=following_table, 
        primaryjoin=following_table.c.follower==id,
        secondaryjoin=following_table.c.followed==id,
        backref="followers")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime())
    content = Column(String(300))
    
    user = relationship("User", backref=backref('posts', order_by=id))

def get_user(userid):
    return session.query(User).filter_by(id=userid).first()

def create_user(username, first_name, last_name):
    user = User(username=username, first_name=first_name, last_name=last_name, created_at=datetime.now())
    session.add(user)
    session.commit()
    return user

def all_posts_for_user(userid):
    #TODO: order by date and add paging and whatever
    return session.query(Post).filter_by(user_id=userid).all()

def create_post(userid, content):
    #todo: validate that user exists somewhere
    post = Post(user_id=userid, content=content, created_at=datetime.now())
    session.add(post)
    session.commit()
    return post

def add_follower(following_user, followed_user):
    following_user.following.append(followed_user)
    session.commit()

def remove_follower(following_user, followed_user):
    following_user.following.remove(followed_user)
    session.commit()

# list of all posts by all users that the given user follows
def get_feed(user):
    # this is implemented in the dumbest way possible because sqlalchemy is dumb
    all_posts = []
    for followee in user.following:
        all_posts.extend(all_posts_for_user(followee.id))

    return sorted(all_posts, key=lambda post: post.created_at)

def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
