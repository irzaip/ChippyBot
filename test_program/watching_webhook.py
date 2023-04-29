import time
import httpx
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the webhook endpoint URL and token
WEBHOOK_URL = "http://localhost:8000/webhook"
TOKEN = "your_token_here"

class Watcher(FileSystemEventHandler):
    def on_modified(self, event):
        # Only trigger on file changes to avoid unnecessary requests
        #if event.is_directory or not event.src_path.endswith('.txt'):
        #    return

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
        print("check..")
        response = httpx.post(WEBHOOK_URL, json=data, headers=headers)
        response.raise_for_status()

if __name__ == "__main__":
    # Set up the file system event handler and observer
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)

    # Start the observer and run indefinitely with a 10-minute sleep interval
    observer.start()
    try:
        while True:
            time.sleep(6)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()