import json
import threading
import requests


class ZygnWebSocketClient:
    def __init__(
        self,
        url,
        token,
        employee_id,
        on_open=None,
        on_identified=None,
        on_close=None,
        on_error=None,
        on_message=None,
    ):
        self.url = url
        self.token = token
        self.employee_id = employee_id
        self.on_open = on_open
        self.on_identified = on_identified
        self.on_close = on_close
        self.on_error = on_error
        self.on_message = on_message
        self._app = None
        self._thread = None
        self._lock = threading.Lock()

    def connect(self):
        if not self.token:
            if self.on_error:
                self.on_error("Missing ZYGN_ACCESS_TOKEN")
            return

        with self._lock:
            if self._thread and self._thread.is_alive():
                return

            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def disconnect(self):
        with self._lock:
            app = self._app

        if app:
            app.close()

    def _run(self):
        try:
            import websocket
        except ImportError:
            if self.on_error:
                self.on_error("Missing dependency: install websocket-client")
            if self.on_close:
                self.on_close()
            return

        self._app = websocket.WebSocketApp(
            self.url,
            on_open=self._handle_open,
            on_close=self._handle_close,
            on_error=self._handle_error,
            on_message=self._handle_message,
        )

        try:
            self._app.run_forever()
        finally:
            with self._lock:
                self._app = None

    def _handle_open(self, ws):
        if self.on_open:
            self.on_open()

    def _handle_close(self, ws, status_code, message):
        if self.on_close:
            self.on_close()

    def _handle_error(self, ws, error):
        if self.on_error:
            self.on_error(str(error))

    def _handle_message(self, ws, message):
        parsed_message = self._parse_message(message)

        if parsed_message.get("type") == "connection_ack":
            self._send_identification(ws)

        elif parsed_message.get("type") == "tallyPayload":
            print("Received tallyPayload:")
            print(parsed_message.get("payload"))

            try:
                response = requests.post(
                    "http://localhost:9000",
                    data=parsed_message.get("payload"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8"
                    },
                    timeout=30,
                )

                print(f"Tally Response ({response.status_code}):")
                print(response.text)

            except requests.RequestException as e:
                print(f"Failed to send payload to Tally: {e}")

        elif parsed_message.get("type") == "error":
            print(f"WebSocket error: {parsed_message.get('payload', 'Unknown error')}")
            if self.on_error:
                self.on_error(str(parsed_message.get("payload", "WebSocket error")))

        if self.on_message:
            self.on_message(parsed_message)

    def _send_identification(self, ws):
        payload = {
            "type": "set_Websocket_Identification",
            "payload": {
                "token": self.token,
                "employeeId": self.employee_id,
            },
            "function": "tallySocket",
        }

        ws.send(json.dumps(payload))

        if self.on_identified:
            self.on_identified()

    def _parse_message(self, message):
        try:
            return json.loads(message)
        except (TypeError, json.JSONDecodeError):
            return {"type": "raw", "payload": message}