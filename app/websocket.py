from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from app.websocket_manager import manager


router = APIRouter(
    tags=["WebSockets"]
)


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
):
    """
    Handle WebSocket connections.
    """

    await manager.connect(
        user_id,
        websocket,
    )

    try:

        while True:

            # Keep the socket alive
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(user_id)