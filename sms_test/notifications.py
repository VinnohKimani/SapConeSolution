import os
import africastalking
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# Initialize Africa's Talking SDK for sandbox environment
africastalking.initialize(
    username="sandbox", # Hardcoded for sandbox environment testing
    api_key=os.getenv('AT_API_KEY')
)
sms = africastalking.SMS

def dispatch_alert(phone_number, message):
    """Sends immediate outbound notifications to passive actors."""
    try:
        # sender_id is optional/ignored in sandbox but required for production shortcodes
        response = sms.send(message, [phone_number])
        print(f"📡 Dispatched Alert to {phone_number} successfully.")
        print(f"📊 SDK Response: {response}\n")
    except Exception as e:
        print(f"❌ Failed to dispatch notification text: {e}")

if __name__ == '__main__':
    # Add a mock phone number with its country code (e.g., "+2547XXXXXXXX")
    mock_proxy = "+254700000001"
    mock_participant = "+254700000002"
    
    print("--- Running LastMile Passive SMS Automation Tests ---\n")
    
    # Sequence A: Countdown Milestone Reminders (Sent to Proxy)
    days_left = [3, 2, 0]
    for day in days_left:
        timing = f"in {day} days" if day > 0 else "TODAY"
        reminder = f"SAPCONE LastMile: Allocation distribution scheduled {timing}. Prepare to locate assigned nomadic clusters."
        print(f"Simulating T-{day} Milestone Trigger...")
        dispatch_alert(mock_proxy, reminder)
        
    # Sequence B: SDP Deposit Notification with OTP
    # Dropped securely to participant, or proxy if participant has no mobile device
    target_device = mock_participant 
    ref_id = "LM-TURK-9821"
    secure_otp = "5831" # Generated cryptographically by backend / smart contract escrow
    
    deposit_alert = f"SAPCONE LastMile: Deposit Confirmed! Ref ID: {ref_id}. Your secret authorization PIN is {secure_otp}. Keep this confidential until cash handover."
    
    print("Simulating SDP Secure Deposit & Transaction Event Key drop...")
    dispatch_alert(target_device, deposit_alert)