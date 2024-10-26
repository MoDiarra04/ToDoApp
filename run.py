from backend import app
from backend import socketio
@app.route('/')
def home():
    return 'Welcome to the homepage!'

if __name__ == '__main__':
    socketio.run(app,debug=True)