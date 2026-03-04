from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mysql, jwt

app = Flask(__name__)
app.config.from_object(Config)

# -------------------------------
# Initialize extensions
# -------------------------------
mysql.init_app(app)
jwt.init_app(app)
CORS(app)

# -------------------------------
# Simple test route
# -------------------------------
@app.route("/")
def home():
    return {"message": "Backend Working"}

# -------------------------------
# Import blueprints AFTER initializing extensions
# -------------------------------
from routes.auth import auth_bp
from routes.farm import farm_bp
from routes.crops import crops_bp
from routes.crop_advisory import advisory_bp  # new blueprint
from routes.expenses import expenses_bp
from routes.mandi import mandi_bp

# -------------------------------
# Register blueprints with URL prefixes
# -------------------------------
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(farm_bp, url_prefix="/api/farm")
app.register_blueprint(crops_bp, url_prefix="/api/crops")
app.register_blueprint(advisory_bp, url_prefix="/api/advisory")  # separate advisory module
app.register_blueprint(expenses_bp, url_prefix="/api/expenses")
app.register_blueprint(mandi_bp, url_prefix="/api/mandi")

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)