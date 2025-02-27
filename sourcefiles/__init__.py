from flask import Flask
import dash

server = Flask(__name__)

server.config['DEBUG'] = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

from sourcefiles import routes