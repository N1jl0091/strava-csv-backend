from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from auth import router as auth_router
from activities import router as activities_router
from config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
from streams import router as streams_router

app.include_router(streams_router)

app = FastAPI()

# Add CORS middleware to allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://n1jl0091.github.io"],  # your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(activities_router)

print(f"Starting app with STRAVA_CLIENT_ID: {STRAVA_CLIENT_ID}")
print(f"STRAVA_CLIENT_SECRET set: {'Yes' if STRAVA_CLIENT_SECRET else 'No'}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting uvicorn on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
