from flask import Flask, request, jsonify
from dataclasses import dataclass
# Initialize Flask application
app = Flask(__name__)

# Basic route for health check/verification
@app.route('/', methods=['GET'])
def home():
    """Root endpoint to verify webhook is running"""
    return "Chatbot Webhook Running!"

# Main webhook endpoint to handle Dialogflow requests
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook handler for Dialogflow requests
    Processes incoming intents and returns appropriate responses
    """
    # Parse incoming JSON with force=True to handle content-type issues
    data = request.get_json(force=True)
    
    # Log received data for debugging
    print("Received webhook data:", data)  # Debugging output

    try:
        # Extract intent name from Dialogflow request
        # Navigate through nested dictionary using get() for safety
        intent_name = data.get("queryResult", {}).get("intent", {}).get("displayName", "")

        # Check if we have a valid intent name
        if intent_name:
            # Construct response text
            response_text = f"Webhook received intent: {intent_name}"
            
            # Return formatted response for Dialogflow
            return jsonify({
                "fulfillmentText": response_text
            })
        else:
            # If no intent is found, return the received data
            return jsonify({
                "status": "success",
                "received": data
            }), 200
            
    except Exception as e:
        # Log any errors for debugging
        print(f"Error processing webhook request: {str(e)}")
        return jsonify({
            "fulfillmentText": "Sorry, I encountered an error processing your request."
        }), 500

# Run the Flask application if this file is run directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    

    # Add at the top of the file
def handle_car_recommendation(data):
    """
    Handle car recommendation intent
    Processes user preferences and returns car suggestions
    """
    parameters = data.get("queryResult", {}).get("parameters", {})
    #Validate requireed paramaeters  required_params = ["budget", "fuel_type", "car_type"]
    is_valid, missing = validate_parameters(parameters, required_params)
    
    if not is_valid:
        return jsonify({
            "fulfillmentText": f"I need more information about: {', '.join(missing)}"
        })
    
    # Get recommendations
    recommendations = get_car_recommendations(
        budget=float(parameters.get("budget", 0)),
        fuel_type=parameters.get("fuel_type"),
        car_type=parameters.get("car_type")
    )
    
    # Format response
    if not recommendations:
        return jsonify({
            "fulfillmentText": "I couldn't find any cars matching your criteria. Would you like to adjust your preferences?"
        })
    
    response_text = "Based on your preferences, here are my recommendations:\n\n"
    for i, car in enumerate(recommendations, 1):
        response_text += f"{i}. {car.make} {car.model}\n"
        response_text += f"   Price: £{car.price:,}\n"
        response_text += f"   Fuel Type: {car.fuel_type}\n"
        response_text += f"   Car Type: {car.car_type}\n\n"
    
    response_text += "Would you like more details about any of these cars?"
    
    return jsonify({
        "fulfillmentText": response_text
    })

def handle_car_specification(data):
    """
    Handle car specification lookup intent
    Returns specific details about requested car
    """
    parameters = data.get("queryResult", {}).get("parameters", {})
    make = parameters.get("Car_Brands")
    model = parameters.get("car_model")
    
    if not make or not model:
        return jsonify({
            "fulfillmentText": "Please provide both the make and model of the car."
        })
    
    # Get car details
    car = get_car_details(make, model)
    
    if not car:
        return jsonify({
            "fulfillmentText": f"Sorry, I couldn't find details for the {make} {model}."
        })
    
    # Format response
    response_text = f"Details for {car.make} {car.model}:\n"
    response_text += f"Price: £{car.price:,}\n"
    response_text += f"Fuel Type: {car.fuel_type}\n"
    response_text += f"Car Type: {car.car_type}\n"
    
    return jsonify({
        "fulfillmentText": response_text
    })

@dataclass
class Car:
    make: str
    model: str
    price: float
    fuel_type: str
    car_type: str
    safety_rating: int = None

cars_database = [
    Car("Toyota", "Yaris", 15000, "Petrol", "Hatchback", 5),
    Car("Honda", "Civic", 20000, "Hybrid", "Sedan", 5),
    Car("Ford", "Focus", 18000, "Diesel", "Hatchback", 4),
    Car("Volkswagen", "Golf", 22000, "Petrol", "Hatchback", 4),
    Car("Tesla", "Model 3", 40000, "Electric", "Sedan", 5)
]

def get_car_recommendations(budget, fuel_type=None, car_type=None):
    """Get car recommendations based on criteria"""
    recommendations = []
    
    for car in cars_database:
        # Check budget
        if car.price > budget:
            continue
        
        # Check fuel type if specified
        if fuel_type and car.fuel_type.lower() != fuel_type.lower():
            continue
        
        # Check car type if specified
        if car_type and car.car_type.lower() != car_type.lower():
            continue
        
        recommendations.append(car)
    
    return recommendations[:5]  # Return top 5 matches

def get_car_details(make, model):
    """Get details for a specific car"""
    for car in cars_database:
        if (car.make.lower() == make.lower() and 
            car.model.lower() == model.lower()):
            return car
    return None
def validate_parameters(parameters, required_params):
    """
    Validate that all required parameters are present
    Returns (is_valid, missing_params)
    """
    missing = [param for param in required_params if not parameters.get(param)]
    return len(missing) == 0, missing
