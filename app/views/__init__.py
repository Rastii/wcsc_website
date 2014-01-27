from app import app, api
from app.database import db_session
from app.models import *
from app.utils import APIResponse
from app.controllers.api import *


#@app.route('/api/blogs', methods=['GET'])
#def get_all_blogs():
#  response = APIResponse(None)
#  return response.get_response(200, [{'test': 'foo bar'}])

api.add_resource(BlogListAPI, '/api/blogs')