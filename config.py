import os


CLOUD_URL = "https://dev-arivu-frontend.rover.zygn.app/"
# CLOUD_URL = "http://localhost:5001"
LOCAL_URL = "http://localhost:9000"
API_BASE_URL = os.getenv("ZYGN_API_BASE_URL", "https://dev-arivu-backend.rover.zygn.app")
WEBSOCKET_URL = "wss://dev-arivu-backend.rover.zygn.app/ws"
# WEBSOCKET_URL = "ws://localhost:5001/ws"

ACCESS_TOKEN = os.getenv("ZYGN_ACCESS_TOKEN", "")
EMPLOYEE_ID = int(os.getenv("ZYGN_EMPLOYEE_ID", "1"))
