from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey

engine = create_engine("sqlite:///moontent.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime())

    #TODO: relationship to posts

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime())
    content = Column(String(300))

def main():
    Base.metadata.create_all(engine)
    # do some stuff

if __name__ == "__main__":
    main()
