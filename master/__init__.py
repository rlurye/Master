from dominate.tags import a
from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config as c

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = c.SECRET_KEY

bootstrap = Bootstrap(app)

from master.logic import views

# if __name__ == '__main__':
#     app.run()