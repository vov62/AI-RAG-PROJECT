from flask import Flask
from flask_cors import CORS
from routes.query_routes import query_bp  
import os

app = Flask(__name__)

# production
ENV = os.getenv("FLASK_ENV", "development")
if ENV == "development":
    # מאפשר CORS ל־localhost כדי שתוכל לבדוק מקומית
    allowed_origins = [
        "http://localhost:4200",
        "http://localhost:8087",
    ]
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
else:
    # Production - אין צורך ב־CORS אם ניגשים דרך אותו Nginx
    print("Running in production mode — CORS disabled (same domain requests).")

# CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

app.register_blueprint(query_bp, url_prefix="/api")

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=(ENV=="development"))