import websocket
from colorama import Fore
import time
import json

def join_vc(token, server, channel, mute, deaf, stream, video):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
    hello = json.loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    ws.send(json.dumps({"op": 2, "d": {"token": token, "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
    ws.send(json.dumps({"op": 4, "d": {"guild_id": server, "channel_id": channel, "self_mute": mute, "self_deaf": deaf, "self_stream?": stream, "self_video": video}}))
    ws.send(json.dumps({"op": 18, "d": {"type": "guild", "guild_id": server, "channel_id": channel, "preferred_region": "singapore"}}))
    ws.send(json.dumps({"op": 1, "d": None}))

    while True:
        try:
            ws.recv()
            time.sleep(heartbeat_interval / 1000)
            ws.send(json.dumps({"op": 1, "d": None}))
        except websocket.WebSocketConnectionClosedException:
            break

    ws.close()