from index import app
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    app.run(host='0.0.0.0')
