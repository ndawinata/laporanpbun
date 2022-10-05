from gevent.pywsgi import WSGIServer
from app import app

app1 = app()
http_server = WSGIServer(("127.0.0.1", 8000), app1)
http_server.serve_forever()