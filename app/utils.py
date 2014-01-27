import logging
from flask import jsonify

class APIResponse:
  ERROR_SQLALCHEMY = "5000"

  WARNINGS = {
    'duplicate': lambda name: "'%s' already exists" % name
  }

  #The constructor should have a logging object with it 
  #to log errors,warnings,etc..
  def __init__(self, logger):
    pass

  #Status codes:
  #   BASIC HTML CODES
  #   200 == NO ERROR
  #   401 == UNAUTHORIZED
  def success(self, data):
    return jsonify({'status': 'SUCCESS', 'data': data})

  def warning(self, warning, data):
    return jsonify({'status': 'WARNING', 'data': data, 'message': warning})

  def error(self, error, error_code):
    return jsonify({'status': 'ERROR', 'error': error})