import os


CLOUD_URL = "https://dev-arivu-frontend.rover.zygn.app/"
# CLOUD_URL = "https://bd0d-2401-4900-94dd-6276-9566-fabc-2472-1455.ngrok-free.app"
LOCAL_URL = "http://localhost:9000"
# WEBSOCKET_URL = "wss://dev-arivu-backend.rover.zygn.app/ws"
WEBSOCKET_URL = "ws://localhost:5001/ws"

ACCESS_TOKEN = os.getenv("ZYGN_ACCESS_TOKEN", "")
EMPLOYEE_ID = int(os.getenv("ZYGN_EMPLOYEE_ID", "1"))
