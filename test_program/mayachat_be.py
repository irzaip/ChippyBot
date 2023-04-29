from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Configure OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define chat endpoint
@app.get("/chat")
async def chat(prompt: str):
    try:
        response = openai.Completion.create(
            engine="ada",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.2,
        )
        return {"text": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))