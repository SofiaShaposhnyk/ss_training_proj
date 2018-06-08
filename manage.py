from app import app
from config import web

if __name__ == '__main__':
    app.app.run(host=web['web_host'], port=web['web_port'], debug=web['debug'])
