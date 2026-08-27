"""WebSocket untuk real-time updates"""

from fastapi import WebSocket, WebSocketDisconnect
import logging
import json
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        """Initialize connection manager"""
        self.active_connections: List[WebSocket] = []
        self.client_subscriptions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def subscribe(self, websocket: WebSocket, channel: str):
        """Subscribe to channel"""
        if channel not in self.client_subscriptions:
            self.client_subscriptions[channel] = []
        
        self.client_subscriptions[channel].append(websocket)
        logger.info(f"Client subscribed to channel: {channel}")

    async def publish(self, channel: str, message: Dict[str, Any]):
        """Publish message to channel"""
        if channel in self.client_subscriptions:
            for connection in self.client_subscriptions[channel]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message: {str(e)}")

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connections"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {str(e)}")


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint
    
    Args:
        websocket: WebSocket connection
        client_id: Client identifier
    """
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe":
                channel = message.get("channel")
                await manager.subscribe(websocket, channel)
                
                await websocket.send_json({
                    "type": "subscription_confirmed",
                    "channel": channel,
                })
            
            elif message.get("type") == "analysis_update":
                # Broadcast analysis updates
                await manager.publish("analysis", {
                    "type": "update",
                    "analysis_id": message.get("analysis_id"),
                    "status": message.get("status"),
                    "timestamp": datetime.now().isoformat(),
                })
            
            elif message.get("type") == "alert":
                # Broadcast alerts
                await manager.publish("alerts", {
                    "type": "vulnerability_detected",
                    "severity": message.get("severity"),
                    "message": message.get("message"),
                    "timestamp": datetime.now().isoformat(),
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client {client_id} disconnected")
