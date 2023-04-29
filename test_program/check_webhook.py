import time
import httpx

# Set the webhook endpoint URL and token
WEBHOOK_URL = "http://localhost:8000/webhook"
TOKEN = "your_token_here"

if __name__ == "__main__":
    while True:
        # Define the data to send in the POST request
        data = {
            "message": "test",
            "sender": "watchdog"
        }

        # Define the headers for the POST request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        }

        # Send the POST request using httpx
        response = httpx.post(WEBHOOK_URL, json=data, headers=headers)
        response.raise_for_status()

        # Sleep for 10 minutes
        time.sleep(6)
