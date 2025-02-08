from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Chatbot Webhook Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)  # Get JSON from Dialogflow request

    # Extract the intent name from the request
    intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName", "")

    # Define responses based on different intents
    response_text = "Webhook received intent: " + intent_name

    return jsonify({"fulfillmentText": response_text})  # Return JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
