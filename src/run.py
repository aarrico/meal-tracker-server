__author__ = 'aarrico'

from src.app import app

app.run(debug=app.config['DEBUG'])