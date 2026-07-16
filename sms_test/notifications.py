import os
import africastalking
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Force load_dotenv to look specifically in this folder's .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Extract and aggressively strip whitespace/newlines from variables
username = os.getenv("AT_USERNAME", "sandbox").strip()
api_key = os.getenv("AT_API_KEY", "").strip()

# Print diagnostic info to help debug auth issues
print("\n🔍 --- DIAGNOSTIC CHECK ---")
print(f"Loaded Username: '{username}'")
print(f"Loaded API Key: '{api_key[:12]}...[HIDDEN]... (Length: {len(api_key)})'")
print("---------------------------\n")

# Define the global Flask variable so 'flask run' can find it!
app = Flask(__name__)

# Initialize Africa's Talking SDK
try:
    africastalking.initialize(
        username=username,
        api_key=api_key
    )
    sms = africastalking.SMS
except Exception as init_err:
    print(f"⚠️ Initialization Error: {init_err}")

def dispatch_alert(phone_number, message):
    """Sends immediate outbound notifications to passive actors."""
    try:
        response = sms.send(message, [phone_number])
        print(f"📡 Dispatched Alert to {phone_number} successfully.")
        print(f"📊 SDK Response: {response}\n")
        return response
    except Exception as e:
        print(f"❌ Failed to dispatch: {e}")
        return None

# --- Flask Endpoints ---

@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    """
    Expects POST request with JSON:
    {
       "phone": "+254700000001",
       "message": "SAPCONE LastMile Notification..."
    }
    """
    data = request.get_json() or {}
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({"error": "Missing 'phone' or 'message' parameters"}), 400
        
    result = dispatch_alert(phone, message)
    if result:
        return jsonify({"status": "success", "sdk_response": result}), 200
    else:
        return jsonify({"status": "failed", "error": "Delivery failed. Check server logs."}), 500

# To run directly with: python notifications.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)