from flask import Flask
from flask_cors import CORS
from routes.query_routes import query_bp  

app = Flask(__name__)

# הפעלת CORS כדי ש- Angular יוכל לגשת ל-API
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

# רישום ה-Blueprint של ה-queries
app.register_blueprint(query_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)