from src.app import app

__author__ = 'padickinson'

app.run(debug=app.config['DEBUG'], port=4990)
