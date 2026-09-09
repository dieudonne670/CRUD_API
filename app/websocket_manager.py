from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    """
    Stores every connected user's WebSocket.

    Key   = user_id

    Value = WebSocket object
    """

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(
        self,
        user_id: int,
        websocket: WebSocket,
    ):
        """
        Accept a new WebSocket connection
        and save it in memory.
        """

        await websocket.accept()

        self.active_connections[user_id] = websocket

        print(f"User {user_id} connected.")

    def disconnect(
        self,
        user_id: int,
    ):
        """
        Remove user after disconnecting.
        """

        if user_id in self.active_connections:

            del self.active_connections[user_id]

            print(f"User {user_id} disconnected.")

    async def send_personal_message(
        self,
        user_id: int,
        message: dict,
    ):
        """
        Send a message to one user.
        """

        websocket = self.active_connections.get(user_id)

        if websocket:

            await websocket.send_json(message)

    async def broadcast(
        self,
        message: dict,
    ):
        """
        Send the same message to every
        connected user.
        """

        for websocket in self.active_connections.values():

            await websocket.send_json(message)

    def is_online(
        self,
        user_id: int,
    ) -> bool:
        """
        Returns True if the user is online.
        """

        return user_id in self.active_connections

    def total_connections(self):

        return len(self.active_connections)


manager = ConnectionManager()

