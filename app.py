from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration (Fetch from Render ENV Variables)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://warevalo:J81Q0NGXCKlUk3Zsm3iUvCTec4Ra1rYx@dpg-cv6q9rrtq21c73dlart0-a.virginia-postgres.render.com:5432/service_costs")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Service Costs Model (Matches Your Table)
class ServiceCost(db.Model):
    __tablename__ = "test_service_costs"  # Match your actual table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(100), nullable=False, unique=True)
    amount_per_unit = db.Column(db.Float, nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)

# Route to Fetch Prices from Database
@app.route('/estimate', methods=['POST'])
def estimate_price():
    data = request.json
    service_name = data.get("service")
    area = float(data.get("area", 0))

    service = ServiceCost.query.filter_by(service_name=service_name).first()
    if service:
        price = service.amount_per_unit * area
        return jsonify({
            "service": service_name,
            "unit": service.unit_of_measure,
            "amount_per_unit": service.amount_per_unit,
            "total_price": round(price, 2)
        })
    else:
        return jsonify({"error": "Service not found"}), 400

@app.route('/')
def home():
    services = ServiceCost.query.with_entities(ServiceCost.service_name).all()
    service_names = [service.service_name for service in services]
    return render_template('index.html', services=service_names)

if __name__ == '__main__':
    app.run(debug=True)