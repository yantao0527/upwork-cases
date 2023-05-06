
If you want to achieve real-time progress updates during file uploads, you can use JavaScript on the frontend with WebSocket for real-time communication between the frontend and the backend. It is an addition and will not disturb the use of original upload.

First, make sure to install neccessary packages:

```
pip install flask flask-socketio gevent gevent-websocket
```

- [upload_progress.py](https://github.com/yantao0527/upwork-cases/blob/main/photos/upload_progress.py)
- [templates/index.html](https://github.com/yantao0527/upwork-cases/blob/main/photos/templates/index.html)

```
python upload_progress.py
```

Demo link: http://127.0.0.1:2200/

AJAX and WebSocket operate independently, and they should not block each other. By using gevent, you're allowing the Flask app to process incoming WebSocket events concurrently with the file upload. The frontend code can remain the same as in previous response, and you should now see real-time updates during the file upload process.

To integrate Flask-SocketIO with Gunicorn, you'll need to use the gevent worker along with the geventwebsocket.gunicorn.workers.GeventWebSocketWorker worker class. First, ensure that you have gevent and gevent-websocket installed:

```
pip install gunicorn gevent gevent-websocket
```

Now, create a new file named wsgi.py in your project directory to define the Flask application instance:

```
from backend import app, socketio

if __name__ == '__main__':
    socketio.run(app)
```

Next, to run the Flask app with Gunicorn and the gevent workers, execute the following command in your terminal or command prompt:

```
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 wsgi:app
```

In this command:

- --worker-class: Specifies the worker class to use, which is set to geventwebsocket.gunicorn.workers.GeventWebSocketWorker.
- -w 1: Sets the number of worker processes to 1 (adjust as needed).
- -b 0.0.0.0:5000: Binds the application to listen on all available interfaces on port 5000.
- wsgi:app: Indicates the location of the Flask application instance.

Now, Gunicorn will serve the Flask application with the gevent worker, enabling it to handle WebSocket connections for real-time communication. The frontend code can remain the same, and you should see real-time updates during the file upload process.
