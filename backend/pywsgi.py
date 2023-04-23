# from gevent import monkey
# monkey.patch_all()

# import os
# from gevent.pywsgi import WSGIServer
# from app import app

# http_server = WSGIServer(('0.0.0.0', 5000), app) # , keyfile='key.pem', certfile='cert.pem')
# http_server.serve_forever()

from waitress import serve
from app import app
serve(app, host="0.0.0.0", port=5000)