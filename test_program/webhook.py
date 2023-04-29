from fastapi import FastAPI, Response
from pydantic import BaseModel
import httpx

app = FastAPI()

TOKEN = "your_token_here"

class Message(BaseModel):
    message: str
    sender: str

async def sendFonnte(data: dict):
    url = "https://api.fonnte.com/send"

    customHeaders = {
        "Content-Type": "application/json",
        "Authorization": TOKEN,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=customHeaders, json=data)
        response.raise_for_status()
        return await response.json()

@app.post("/webhook")
async def webhook(message: Message, response: Response):
    if message.message == "test":
        data = {
            "target": message.sender,
            "message": "working great!"
        }
        await sendFonnte(data)
    else:
        data = {
            "target": message.sender,
            "message": "this is default reply from fonnte"
        }
        await sendFonnte(data)
    return response.status_code(200)