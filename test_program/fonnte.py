import json
import requests

def send_fonnte(target, data):
    url = "https://api.fonnte.com/send"
    headers = {"Authorization": "0Bigfe321Uvrzv-IHtkf"}
    payload = {
        "target": target,
        "message": data["message"],
        "url": data.get("url", ""),
        "filename": data.get("filename", ""),
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text

# Get the JSON data from the request's body
data = json.loads(request.data)

device = data["device"]
sender = data["sender"]
message = data["message"]
member = data["member"]
name = data["name"]
location = data["location"]

# data below will only received by device with all feature package
# start
url = data.get("url", "")
filename = data.get("filename", "")
extension = data.get("extension", "")
# end

if message == "test":
    reply = {"message": "working great!"}
elif message == "image":
    reply = {
        "message": "image message",
        "url": "https://filesamples.com/samples/image/jpg/sample_640%C3%97426.jpg",
    }
elif message == "audio":
    reply = {
        "message": "audio message",
        "url": "https://filesamples.com/samples/audio/mp3/sample3.mp3",
        "filename": "music",
    }
elif message == "video":
    reply = {
        "message": "video message",
        "url": "https://filesamples.com/samples/video/mp4/sample_640x360.mp4",
    }
elif message == "file":
    reply = {
        "message": "file message",
        "url": "https://filesamples.com/samples/document/docx/sample3.docx",
        "filename": "document",
    }
else:
    reply = {
        "message": "Sorry, I don't understand. Please use one of the following keywords: Hello, Audio, Video, Image, File.",
    }

send_fonnte(sender, reply)
