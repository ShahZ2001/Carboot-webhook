from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Chatbot Webhook Running!"

@app.route('/webhook', methods=['POST'])  # <-- ADDED THE DECORATOR
def webhook():
    data = request.get_json(force=True)  # Ensure JSON parsing

    # Check if the request is from Dialogflow
    intent_name = data.get("queryResult", {}).get("intent", {}).get("displayName", "")

    if intent_name:  # If coming from Dialogflow
        response_text = "Webhook received intent: " + intent_name
        return jsonify({"fulfillmentText": response_text})

    # If it's not a Dialogflow request, just return the received data
    return jsonify({"received": data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
