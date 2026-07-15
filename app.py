from flask import Flask, request, make_response

app = Flask(__name__)

# MOCK DATA: Simulating what your database will handle later
MOCK_BENEFICIARIES = {
    "REF1024": {"phone": "+254712345678", "otp": "58210", "amount": 1500},
    "REF5500": {"phone": "+254799887766", "otp": "11223", "amount": 2500}
}

# @app.route('/ussd', methods=['POST'])
# def ussd_gateway():
#     # Africa's Talking sends data via form URL-encoded payload
#     session_id   = request.form.get("sessionId")
#     service_code = request.form.get("serviceCode")
#     phone_number = request.form.get("phoneNumber")
#     text         = request.form.get("text", "")

#     # Parse user inputs separated by '*' (e.g. "REF1024*58210")
#     text_parts = text.split('*') if text else []
#     step = len(text_parts)

@app.route('/ussd', methods=['POST'])
def ussd_gateway():
    # Force reading from form parameters, falling back to arguments or JSON
    session_id   = request.form.get("sessionId") or request.values.get("sessionId")
    service_code = request.form.get("serviceCode") or request.values.get("serviceCode")
    phone_number = request.form.get("phoneNumber") or request.values.get("phoneNumber")
    text         = request.form.get("text", "") or request.values.get("text", "")

    # Clean up the string to remove unexpected spaces
    text = str(text).strip()
    
    text_parts = text.split('*') if text else []
    step = len(text_parts)

    response_msg = ""

    # STEP 0: Entry point
    if step == 0:
        response_msg = "CON Welcome to LastMile.\nPlease enter your Reference ID:"

    # STEP 1: Process Reference ID & Request OTP
    elif step == 1:
        entered_ref = text_parts[0].upper()
        if entered_ref in MOCK_BENEFICIARIES:
            response_msg = "CON Enter the active Transaction OTP sent via SMS:"
        else:
            response_msg = "END Error: Reference ID not found in our systems."

    # STEP 2: Validate OTP & Present Confirmation Screen
    elif step == 2:
        entered_ref = text_parts[0].upper()
        entered_otp = text_parts[1]
        record = MOCK_BENEFICIARIES.get(entered_ref)

        if record and record["otp"] == entered_otp:
            response_msg = f"CON Confirm withdrawal of {record['amount']} KES to proxy wallet ({phone_number})?\n1. Confirm\n2. Cancel"
        else:
            response_msg = "END Error: Invalid Verification OTP."

    # STEP 3: Handle Action Selection
    elif step == 3:
        selection = text_parts[2]
        entered_ref = text_parts[0].upper()
        record = MOCK_BENEFICIARIES.get(entered_ref)

        if selection == "1" and record:
            # FUTURE INJECTION: Trigger Stellar/Soroban swap and dispatch Fiat Mobile Money
            print(f"DEBUG: Initiating M-Pesa push for {record['amount']} KES...")
            response_msg = f"END Payout of {record['amount']} KES authorized! Funds are being routed to your mobile money wallet."
        else:
            response_msg = "END Transaction cancelled by user."

    # USSD Gateways strictly expect plain-text responses
    response = make_response(response_msg, 200)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == '__main__':
    # Running on port 3000 to match your Ngrok/Localhost setups
    app.run(port=3000, debug=True)