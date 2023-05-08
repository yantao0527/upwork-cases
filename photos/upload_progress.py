from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('photos')

    for file in files:
        filename = file.filename
        # conduct upload
        time.sleep(5)
        print(filename)

    return 'All files uploaded successfully'

@app.route('/upload2', methods=['POST'])
def upload_files2():
    socketio.emit('total_files', {'total': 0})
    
    files = request.files.getlist('photos')
    
    total_files = len(files)
    socketio.emit('total_files', {'total': total_files})

    sn = 0
    for file in files:
        filename = file.filename
        # conduct upload
        time.sleep(5)
        print(filename)
        sn += 1
        socketio.emit('uploaded_file', {
                'total': total_files,
                'sn': sn,
                'filename': filename,
            })

    socketio.emit('upload_complete', {})
    return 'File upload in progress'

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=2200)
