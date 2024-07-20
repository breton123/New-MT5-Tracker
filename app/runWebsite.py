from flask_cors import CORS
from app import create_app

def run():
    app = create_app()
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})


    app.run(debug=False, use_reloader=False)
