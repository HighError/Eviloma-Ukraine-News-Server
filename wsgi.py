from index import app
from dotenv import load_dotenv
from werkzeug.serving import WSGIRequestHandler

if __name__ == "__main__":
    load_dotenv()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host='0.0.0.0')
