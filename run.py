import sys
from app import app

if len(sys.argv) == 1:
  app.run(host='0.0.0.0', debug = True)
else:
  #Use this to setup the DB
  if sys.argv[1] == 'setup':
      from app.database import *
      kill_db()
      init_db()
      setup_db()
      sys.exit()
  #Use this to setup python shell
  elif sys.argv[1] == 'shell':
    from flask import *
    from app import *
    from app.models import *
    from IPython import embed
    embed()
    sys.exit()

sys.exit()