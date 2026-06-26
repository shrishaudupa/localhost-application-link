import os


CLOUD_URL = "https://dev-arivu-frontend.rover.zygn.app/"
LOCAL_URL = "http://localhost:9000"
WEBSOCKET_URL = "wss://dev-arivu-backend.rover.zygn.app/ws"

ACCESS_TOKEN = os.getenv("ZYGN_ACCESS_TOKEN", "")
EMPLOYEE_ID = int(os.getenv("ZYGN_EMPLOYEE_ID", "1"))
