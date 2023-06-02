from flask import Flask
import datetime
import socket

app = Flask(__name__)

@app.route('/')
def get_timestamp_hostname():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hostname = socket.gethostname()
    response = f'Timestamp: {timestamp}\nHostname: {hostname}\n'
    return response

if __name__ == '__main__':
    app.run()