from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook is running successfully!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)
    return jsonify({"status": "success", "data": data}), 200

if __name__ == "__main__":
    app.run(debug=True)
