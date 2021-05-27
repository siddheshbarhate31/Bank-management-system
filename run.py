from app import app
from app.route import *
from app.common.logging import *
from app.model import *
from app import manager

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    manager.run()
