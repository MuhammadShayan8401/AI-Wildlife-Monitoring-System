from flask import Flask
from flask_cors import CORS
from config import Config
from db import mysql

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
CORS(app)

# Import routes AFTER initializing mysql
from routes.animals import animals_bp
from routes.enclosures import enclosures_bp
from routes.feeding import feeding_bp
from routes.health import health_bp
from routes.behavior import behavior_bp
from routes.dashboard import dashboard_bp
from routes.alerts import alerts_bp
from routes.health_risk import risk_bp
from routes.stress_monitor import stress_bp
from routes.behavior_logs import behavior_logs_bp

# Register routes
app.register_blueprint(animals_bp)
app.register_blueprint(enclosures_bp)
app.register_blueprint(feeding_bp)
app.register_blueprint(health_bp)
app.register_blueprint(behavior_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(risk_bp)
app.register_blueprint(stress_bp)
app.register_blueprint(behavior_logs_bp)

if __name__ == "__main__":
    app.run(debug=True)