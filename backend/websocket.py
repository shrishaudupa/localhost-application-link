import asyncio
import json
import websockets

# WS_URL = "wss://dev-arivu-backend.rover.zygn.app/ws"
WS_URL = "wss://7e40-2401-4900-892f-c2ad-4d7b-7b0b-473d-fcb1.ngrok-free.app/ws"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxODIsImVtYWlsIjoic2hyaXNoYUBnbWFpbC5jb20iLCJmdWxsbmFtZSI6IlNocmlzaGEgVWR1cGEiLCJpbml0aWFscyI6IlNVIiwidXNlclR5cGUiOiJFbXBsb3llZSIsImVtcGxveWVlSWQiOjM3MiwiY29tcGFueUlkIjo4MDAxMywiZmlyc3ROYW1lIjoiU2hyaXNoYSIsImxhc3ROYW1lIjoiVWR1cGEiLCJtb2JpbGVOdW1iZXIiOiI3MDIyNjMwMTgwIiwiZW1wbG95ZWVFbWFpbElkIjoic2hyaXNoYUBnbWFpbC5jb20iLCJlbXBsb3llZU51bWJlciI6IkVNUDgwMDEzLTAwMDAxIiwiYWNjZXNzIjoiRW5hYmxlZCIsImF0dGVuZGFuY2UiOiJFbmFibGVkIiwidmlzaXRvcklkIjoiODUwMTczOWNmNzM0NGZmODYyZjQ1NzE3YmEwOTZkMjIiLCJjb21wYW55TmFtZSI6IlNocmlzaGEgRGV2ZWxvcG1lbnQgQ29tcGFueSIsInRvTWFpbCI6IkFkbWluIiwiZW1wbG95ZWVUeXBlIjoiQWRtaW4iLCJjb21wYW55U3RhdHVzIjoiQWN0aXZlIiwiY29tcGFueVR5cGUiOiJDdXN0b21lciIsImNvbXBhbnlnc3ROdW1iZXIiOiI4OTEzOTkzMTMxNDE0MTQiLCJjb21wYW55UmVnaXN0ZXJlZFllYXIiOjIwMjYsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5IjoiSW5kaWEifSwiZW1wbG95ZWVSb2xlcyI6W3sidGVhbSI6IkFkbWluIiwicm9sZSI6Ik1hbmFnZXIifSx7InRlYW0iOiJTYWxlcyIsInJvbGUiOiJNYW5hZ2VyIn0seyJ0ZWFtIjoiRGVzaWduIiwicm9sZSI6Ik1hbmFnZXIifSx7InRlYW0iOiJQcm9jdXJlbWVudCIsInJvbGUiOiJNYW5hZ2VyIn0seyJ0ZWFtIjoiT25zaXRlIiwicm9sZSI6Ik1hbmFnZXIifSx7InRlYW0iOiJIUiIsInJvbGUiOiJNYW5hZ2VyIn0seyJ0ZWFtIjoiSW52ZW50b3J5Iiwicm9sZSI6Ik1hbmFnZXIifSx7InRlYW0iOiJBY2NvdW50cyIsInJvbGUiOiJNYW5hZ2VyIn1dLCJpYXQiOjE3ODI0NDI4MDQsImV4cCI6MTc4MjQ4NjAwNH0.QBhXgVhPg99RzCcbxQvWEEykihaIbZ5XyQ_xWSLNcN4"
EMPLOYEE_ID = 1

async def main():
    async with websockets.connect(WS_URL) as ws:
        print("Connected")

        # Receive connection acknowledgement
        msg = await ws.recv()
        print("Server:", msg)

        # Authenticate
        auth = {
            "type": "set_Websocket_Identification",
            "payload": {
                "token": TOKEN,
                "employeeId": EMPLOYEE_ID
            }
        }

        await ws.send(json.dumps(auth))
        print("Authentication sent")

        # Listen for messages
        while True:
            message = await ws.recv()
            print("Received:", message)

asyncio.run(main())