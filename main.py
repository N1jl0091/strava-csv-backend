from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os
import requests
import uuid

app = FastAPI()
SESSIONS = {}

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "https://strava-csv-backend-production.up.railway.app/callback"

print(f"Starting app with STRAVA_CLIENT_ID: {STRAVA_CLIENT_ID}")
print(f"STRAVA_CLIENT_SECRET set: {'Yes' if STRAVA_CLIENT_SECRET else 'No'}")

@app.get("/auth")
def auth():
    print("Received request to /auth endpoint")
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        print("ERROR: STRAVA_CLIENT_ID or STRAVA_CLIENT_SECRET not set")
        return {"error": "Server configuration error"}
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=activity:read_all"
    )
    print(f"Redirecting user to Strava auth URL: {url}")
    return RedirectResponse(url)


@app.get("/callback")
def callback(request: Request, code: str):
    print(f"Received callback with code: {code}")
    token_response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })

    print(f"Strava token response status: {token_response.status_code}")
    try:
        token_data = token_response.json()
        print(f"Token data received: {token_data}")
    except Exception as e:
        print(f"Failed to decode token response JSON: {e}")
        return {"error": "Failed to parse token response"}

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = token_data
    print(f"Created session {session_id} with token data")

    redirect_url = f"https://N1jl0091.github.io/strava-csv-frontend/activities.html?session_id={session_id}"
    print(f"Redirecting user to frontend URL: {redirect_url}")
    return RedirectResponse(redirect_url)
