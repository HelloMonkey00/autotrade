from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from backend.route import route_bp
import sys

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.register_blueprint(route_bp, url_prefix='/api')

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print(sys.path)
    socketio.run(app, debug=True)