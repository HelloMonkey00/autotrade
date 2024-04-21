from flask import Flask, render_template
from backend.route import route_bp

from backend import socketio

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.register_blueprint(route_bp, url_prefix='/api')

socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005)