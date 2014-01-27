from app import app
from app import api
from app.database import db_session
from flask.ext.restful import Resource, reqparse
from app.models import *
from app.utils import APIResponse
from sqlalchemy import exc


class BlogListAPI(Resource):
  def __init__(self):
    self.response = APIResponse(None)

  def get(self):
    blogs = db_session.query(Blog).all()

    return self.response.success(\
      [blog.to_dict(edits=True,labels=True) for blog in blogs])

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('content', type=str, required=True)
    parser.add_argument('labels', type=int, required=False, action="append")
    args = parser.parse_args()
    labels = []
    try:
      #Checks for duplicate
      if db_session.query(Blog).filter(Blog.title.ilike("%"+args.title+"%"))\
                   .first() is not None:
        return self.response.warning(\
          self.response.WARNINGS['duplicate'](args.title), None)
      #Check of the labels exist
      for label in args.labels:
        label_instance = db_session.query(BlogLabel).get(label)
        if label_instance is None:
          return self.response.warning("Label with id %d does not exist." % label, 
                                       None)
        labels.append(label_instance)

      blog = Blog(title=args.title,
                  author_id=1, #TODO: Change this to user's current session
                  content=args.content)
      #Now append the labels to the blog
      for label_instance in labels:
        blog.labels.append(label_instance) 
      db_session.add(blog)
      db_session.commit()
      return self.response.success(None)
    except exc.SQLAlchemyError:
      return self.response.error('Error creating new blog', 
                                          self.response.ERROR_SQLALCHEMY)