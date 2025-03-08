from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample pricing data
SERVICE_PRICES = {
    "roofing": 5.0,
    "painting": 2.5,
    "power_washing": 1.0
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate_price():
    data = request.json
    service = data.get("service")
    area = float(data.get("area", 0))

    if service in SERVICE_PRICES:
        price = SERVICE_PRICES[service] * area
        return jsonify({"estimated_price": round(price, 2)})
    else:
        return jsonify({"error": "Service not found"}), 400

if __name__ == '__main__':
    app.run(debug=True)