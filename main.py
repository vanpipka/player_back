import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services.player_core.soundMusicCore import get_all_track, get_styles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/playlists/")
async def playlists():

    return JSONResponse(content={"count": 1, "items": get_styles()})


@app.get("/tracks/{style}")
async def get_track(style: str):
    tracks: list = get_all_track(style)

    return JSONResponse(content={"count": len(tracks), "data": tracks})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

