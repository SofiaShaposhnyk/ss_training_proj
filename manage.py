from app import app
from config import web

if __name__ == '__main__':
    app.app.run(host=web['host'], port=web['port'], debug=web['debug'])
