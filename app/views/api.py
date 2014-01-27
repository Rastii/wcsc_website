from . import app, api
from app.controllers.api import *

#@app.route('/api/blogs', methods=['GET'])
#def get_all_blogs():
#  response = APIResponse(None)
#  return response.get_response(db_session.query(Blog).all())

api.add_resource('BlogAPI', '/blogs/<blog_id>')