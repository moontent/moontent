from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from datetime import datetime

engine = create_engine("sqlite:///moontent.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime())

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

def main():
    Base.metadata.create_all(engine)
    # do some stuff

if __name__ == "__main__":
    main()
