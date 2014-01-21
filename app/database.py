from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///dev.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, 
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from app.models import *

def init_db():
    Base.metadata.create_all(engine)

def kill_db():
    Base.metadata.drop_all(engine)

def setup_db():
    from app.models import *
    """User Creation
    """
    user = User(uname='user', email='user@user.com', password='123456')
    db_session.add(user)
    db_session.commit()

    """Label Creation
    """
    label1 = BlogLabel(title="general")
    db_session.add(label1)
    db_session.commit()
    """Blog Creation
    """
    blog1 = Blog(title='blog title', content='blog content', author=user.id)
    blog1.labels.append(label1)
    db_session.add(blog1)
    db_session.commit()


