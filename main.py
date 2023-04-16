from fastapi import FastAPI
from controller import user, auth
from config import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi import WebSocket, BackgroundTasks, WebSocketDisconnect
from controller.websocket.notifier import notifier
import json

app = FastAPI()
app.config = config

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user.router, prefix=f"/user")
app.include_router(auth.router, prefix=f"/auth")


@app.websocket("/socket/ws/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket, room_name, background_tasks: BackgroundTasks
):
    await notifier.connect(websocket, room_name)
    try:
        while True:
            data = await websocket.receive_text()
            d = json.loads(data)
            d["room_name"] = room_name

            room_members = (
                notifier.get_members(room_name)
                if notifier.get_members(room_name) is not None
                else []
            )
            if websocket not in room_members:
                print("SENDER NOT IN ROOM MEMBERS: RECONNECTING")
                await notifier.connect(websocket, room_name)

            await notifier._notify(f"{data}", room_name)
    except WebSocketDisconnect:
        notifier.remove(websocket, room_name)