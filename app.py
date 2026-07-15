from flask import Flask, request, make_response

app = Flask(__name__)

MOCK_BENEFICIARIES = {
    "1024": {"name": "John", "phone": "+254712345678", "otp": "58210", "amount": 15000, "is_proxy": False},
    "5500": {"name": "Mary", "phone": "+254799887766", "otp": "11223", "amount": 25000, "is_proxy": True},
    "9900": {"name": "Joseph", "phone": "+254799887766", "otp": "44556", "amount": 18000, "is_proxy": True} # Shares phone with Mary
}

STRINGS = {
    "en": {
        "welcome": "CON Welcome to LastMile.\nSelect Language:\n1. English\n2. Kiswahili",
        "enter_ref": "CON Enter your 4-digit Reference ID:",
        "enter_otp": "CON Enter the active Transaction OTP sent to your phone:",
        "select_user": "CON Multiple users found on this phone. Select your name:\n",
        "confirm_payout": "CON Withdraw {amount} KES to phone {phone}?\n1. Confirm\n2. Cancel",
        "authorized": "END Payout of {amount} KES authorized! Funds are being sent to your mobile wallet.",
        "cancelled": "END Transaction cancelled.",
        "err_ref": "END Error: Reference ID not found.",
        "err_otp": "END Error: Invalid Verification OTP.",
        "invalid_opt": "END Invalid selection."
    },
    "sw": {
        "welcome": "CON Karibu LastMile.\nChagua Lugha:\n1. English\n2. Kiswahili",
        "enter_ref": "CON Weka Nambari yako ya Ushahidi (Ref ID):",
        "enter_otp": "CON Weka nambari ya siri (OTP) uliyotumiwa kwa SMS:",
        "select_user": "CON Chagua jina lako kwenye orodha:\n",
        "confirm_payout": "CON Kubali kutoa KES {amount} kwenda nambari {phone}?\n1. Kubali\n2. Ghairi",
        "authorized": "END Malipo ya KES {amount} yamekubaliwa! Fedha zinatumwa kwenye simu yako hivi punde.",
        "cancelled": "END Shughuli imenghairiwa.",
        "err_ref": "END Makosa: Nambari ya Ushahidi haipatikani.",
        "err_otp": "END Makosa: Nambari ya siri (OTP) sio sawa.",
        "invalid_opt": "END Chaguo si sahihi."
    }
}

@app.route('/ussd', methods=['POST'])
def ussd_gateway():
    phone_number = request.form.get("phoneNumber") or request.values.get("phoneNumber", "")
    text         = request.form.get("text", "") or request.values.get("text", "")
    text         = str(text).strip()
    
    text_parts = text.split('*') if text else []
    step = len(text_parts)

    response_msg = ""

    if step == 0:
        return respond(STRINGS["en"]["welcome"]) 

    lang_choice = text_parts[0]
    lang = "sw" if lang_choice == "2" else "en" # Fallback to English

    matching_accounts = {k: v for k, v in MOCK_BENEFICIARIES.items() if v["phone"] == phone_number}
    
    if step == 1:
        if not matching_accounts:
            # If the phone isn't registered, prompt manual entry of Reference ID
            response_msg = STRINGS[lang]["enter_ref"]
        elif len(matching_accounts) == 1:
            # Direct User Flow: Single account matches caller ID. Skip Ref ID and ask for OTP!
            response_msg = STRINGS[lang]["enter_otp"]
        else:
            # Proxy Flow: Multiple beneficiaries share this phone. Present a clean selection menu.
            menu = STRINGS[lang]["select_user"]
            for idx, (ref, acc) in enumerate(matching_accounts.items(), 1):
                menu += f"{idx}. {acc['name']}\n"
            response_msg = f"CON {menu.strip()}"

    elif step == 2:
        user_input = text_parts[1]
        
        if not matching_accounts:
            entered_ref = user_input.upper()
            if entered_ref in MOCK_BENEFICIARIES:
                response_msg = STRINGS[lang]["enter_otp"]
            else:
                response_msg = STRINGS[lang]["err_ref"]
                
        elif len(matching_accounts) == 1:

            ref_id = list(matching_accounts.keys())[0]
            record = MOCK_BENEFICIARIES[ref_id]
            if record["otp"] == user_input:
                response_msg = STRINGS[lang]["confirm_payout"].format(amount=record["amount"], phone=phone_number)
            else:
                response_msg = STRINGS[lang]["err_otp"]
                
        else:
            try:
                selected_index = int(user_input) - 1
                ref_id = list(matching_accounts.keys())[selected_index]
                response_msg = STRINGS[lang]["enter_otp"]
            except (ValueError, IndexError):
                response_msg = STRINGS[lang]["invalid_opt"]

    elif step == 3:
        user_input = text_parts[2]
        
        if not matching_accounts:
            ref_id = text_parts[1].upper()
            record = MOCK_BENEFICIARIES.get(ref_id)
            if record and record["otp"] == user_input:
                response_msg = STRINGS[lang]["confirm_payout"].format(amount=record["amount"], phone=phone_number)
            else:
                response_msg = STRINGS[lang]["err_otp"]
                
        elif len(matching_accounts) == 1:
            ref_id = list(matching_accounts.keys())[0]
            record = MOCK_BENEFICIARIES[ref_id]
            if user_input == "1":
                response_msg = STRINGS[lang]["authorized"].format(amount=record["amount"])
            else:
                response_msg = STRINGS[lang]["cancelled"]
                
        else:
            try:
                selected_index = int(text_parts[1]) - 1
                ref_id = list(matching_accounts.keys())[selected_index]
                record = MOCK_BENEFICIARIES[ref_id]
                if record["otp"] == user_input:
                    response_msg = STRINGS[lang]["confirm_payout"].format(amount=record["amount"], phone=phone_number)
                else:
                    response_msg = STRINGS[lang]["err_otp"]
            except (ValueError, IndexError):
                response_msg = STRINGS[lang]["invalid_opt"]

    elif step == 4:
        user_input = text_parts[3]
        if not matching_accounts:
            ref_id = text_parts[1].upper()
        else:
            selected_index = int(text_parts[1]) - 1
            ref_id = list(matching_accounts.keys())[selected_index]
            
        record = MOCK_BENEFICIARIES.get(ref_id)
        if user_input == "1" and record:
            print(f"DEBUG PAYOUT: Sending KES {record['amount']} to {phone_number}...")
            response_msg = STRINGS[lang]["authorized"].format(amount=record["amount"])
        else:
            response_msg = STRINGS[lang]["cancelled"]

    return respond(response_msg)

def respond(message):
    response = make_response(message, 200)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)