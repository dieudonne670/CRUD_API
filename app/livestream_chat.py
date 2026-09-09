from collections import defaultdict

from fastapi import WebSocket


class LiveChatManager:

    def __init__(self):

        self.rooms = defaultdict(list)

    async def connect(
        self,
        stream_id: int,
        websocket: WebSocket,
    ):

        await websocket.accept()

        self.rooms[stream_id].append(websocket)

    def disconnect(
        self,
        stream_id: int,
        websocket: WebSocket,
    ):

        if websocket in self.rooms[stream_id]:

            self.rooms[stream_id].remove(websocket)

    async def broadcast(
        self,
        stream_id: int,
        message: dict,
    ):

        dead_connections = []

        for connection in self.rooms[stream_id]:

            try:

                await connection.send_json(message)

            except Exception:

                dead_connections.append(connection)

        for connection in dead_connections:

            self.disconnect(stream_id, connection)


live_chat_manager = LiveChatManager()