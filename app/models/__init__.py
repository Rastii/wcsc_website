from sqlalchemy import Table, Column, ForeignKey, Integer, String,\
Boolean, Text, DateTime, func
from sqlalchemy.orm import relationship, backref, deferred
from app.database import Base, db_session
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

TIMESTRING = "%Y-%m-%dT%H:%M:%S"

blog_labels = Table('blog_labels', Base.metadata,
  Column('blog_id', Integer, ForeignKey('blogs.id')),
  Column('label_id', Integer, ForeignKey('blog_label_catalog.id')))

blog_edits = Table('blog_edits', Base.metadata,
  Column('edit_id', Integer, ForeignKey('blog_edit_catalog.id')),
  Column('blog_id', Integer, ForeignKey('blogs.id')))

class User(Base):
  #Custom attribute to define user selectable fields since
  #optional field selection will be allowed for all API
  user_fields = [
    "id", 
    "uname", 
    "email", 
    "password", 
    "blog_submissions"
  ]
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

  def to_dict(self):
    to_return = {}
    if self.id: to_return['id'] = self.id
    if self.uname: to_return['uname'] = self.uname
    if self.email: to_return['email'] = self.email
    if self.password: to_return['password'] = self.password
    if self.enabled: to_return['enabled'] = self.enabled
    if self.blog_submissions: 
      to_return['blog_submissions'] = [
        {
          'id': blog.id,
          'title': blog.title
        } for blog in self.blog_submissions]
    return to_return

class Blog(Base):
  #Custom attribute to define user selectable fields since
  #optional field selection will be allowed for all API
  user_fields = [
    "id",
    "title",
    "content",
    "author",
    "submission_time",
    "labels",
    "edits"
  ]
  __tablename__ = 'blogs'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  content = Column(Text())
  author_id = Column(Integer, ForeignKey('users.id'))
  author = relationship(User, backref=backref('blogs', lazy='dynamic', uselist=False))
  submission_time = Column(DateTime(timezone=False), default=datetime.datetime.now())
  labels = relationship("BlogLabel", secondary="blog_labels")
  edits = relationship("BlogEdit", secondary="blog_edits")

  def to_dict(self, **kwargs):
    display_labels = kwargs.get('labels', False)
    display_edits = kwargs.get('edits', False)
    to_return = {}
    if self.id: 
      to_return['id'] = self.id
    if self.title: 
      to_return['title'] = self.title
    if self.content: 
      to_return['content'] = self.content
    if self.author_id: 
      to_return['author'] = {'id': self.author.id,'uname': self.author.uname}
    if self.submission_time: 
      to_return['submission_time'] = self.submission_time.strftime(TIMESTRING)
    if display_labels is True:
      to_return['labels'] = [{'id': label.id, 'title': label.title} for label in self.labels]
    if display_edits is True:
      to_return['edits'] = [{'id': edit.id, 'edit_time': edit.edit_time.strftime(TIMESTRING)}
                            for edit in self.edits]

    return to_return

class BlogLabel(Base):
  user_fields = [
    "id",
    "title"
  ]
  __tablename__ = 'blog_label_catalog'
  id = Column(Integer, primary_key=True)
  title = Column(String(64), unique=True)

class BlogEdit(Base):
  __tablename__ = 'blog_edit_catalog'
  id = Column(Integer, primary_key=True)
  edit_time = Column(DateTime(timezone=False), default=datetime.datetime.now())
  editor_id = Column(Integer, ForeignKey('users.id'))
  editor = relationship(User, backref=backref('blog_edit_catalog', lazy='dynamic'))

class Event(Base):
  user_fields = [
    "id",
    "title",
    "description",
    "link"
  ]
  __tablename__ = 'events'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  description = Column(Text())
  link = Column(String(256))