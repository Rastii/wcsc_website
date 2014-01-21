from sqlalchemy import Table, Column, ForeignKey, Integer, String,\
Boolean, Text, DateTime, func
from sqlalchemy.orm import relationship, backref, deferred
from app.database import Base, db_session
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

blog_labels = Table('blog_labels', Base.metadata,
  Column('blog_id', Integer, ForeignKey('blogs.id')),
  Column('label_id', Integer, ForeignKey('blog_label_catalog.id')))

blog_edits = Table('blog_edits', Base.metadata,
  Column('edit_id', Integer, ForeignKey('blog_edit_catalog.id')),
  Column('blog_id', Integer, ForeignKey('blogs.id')))

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  uname = Column(String(32), unique=True)
  email = Column(String(64), unique=True)
  password = deferred(Column(String(60)))
  enabled = deferred(Column(Boolean, default=True)) #TODO: Add mail daemon to confirm user
  blog_submissions = relationship("Blog", backref="users")

  def __repr__(self):
    return '< User(uname: %s, email: %s, enabled: %s) >' %\
      (self.uname, self.email, self.enabled)

  #Required methods for flask user login
  def get_id(self):
    return unicode(self.id)

  def is_active(self):
    return self.enabled

  def is_anonymouse(self):
    return False

  def is_authenticated(self):
    return True

class Blog(Base):
  __tablename__ = 'blogs'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  content = Column(Text())
  author = Column(Integer, ForeignKey('users.id'))
  submission_time = Column(DateTime(timezone=False), default=datetime.datetime.now())
  labels = relationship("BlogLabel", secondary="blog_labels")
  edits = relationship("BlogEdit", secondary="blog_edits")

  def __repr__(self):
    return '< Blog(title: %s, content: %s, author: %d, submission_time: %s) >' %\
      (self.title, self.content, self.author, self.submission_time)

class BlogLabel(Base):
  __tablename__ = 'blog_label_catalog'
  id = Column(Integer, primary_key=True)
  title = Column(String(64), unique=True)

class BlogEdit(Base):
  __tablename__ = 'blog_edit_catalog'
  id = Column(Integer, primary_key=True)
  edit_time = Column(DateTime(timezone=False), default=datetime.datetime.now())
  editor = Column(Integer, ForeignKey('users.id'))

class Event(Base):
  __tablename__ = 'events'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  description = Column(Text())
  link = Column(String(256))