from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os
import requests
import uuid

app = FastAPI()
SESSIONS = {}

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "https://YOUR_BACKEND.onrailway.app/callback"

@app.get("/auth")
def auth():
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=activity:read_all"
    )
    return RedirectResponse(url)

@app.get("/callback")
def callback(request: Request, code: str):
    token_response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })

    token_data = token_response.json()
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = token_data

    return RedirectResponse(f"https://yourusername.github.io/strava-csv-frontend/activities.html?session_id={session_id}")
