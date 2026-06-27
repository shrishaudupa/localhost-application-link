import tkinter as tk
from tkinter import ttk

from config import CLOUD_URL , LOCAL_URL, WEBSOCKET_URL
from tunnel.websocket_client import ZygnWebSocketClient

STATUS_DISCONNECTED = "disconnected"
STATUS_CONNECTING = "connecting"
STATUS_AUTHENTICATING = "authenticating"
STATUS_CONNECTED = "connected"
STATUS_ERROR = "error"
STATUS_DOT = "\u25cf"


class zygnConnectorApp(tk.Tk):
    def __init__(self, auth_session):
        super().__init__()

        self.auth_session = auth_session
        self.status = STATUS_DISCONNECTED
        self.last_error = None
        self.websocket_client = None

        self.title("ZYGN CONNECTOR")
        self.geometry("420x360")
        self.minsize(360, 320)
        self.resizable(False, False)
        self.configure(bg="#f6f7f9")
        self.protocol("WM_DELETE_WINDOW", self._handle_window_close)

        self._configure_styles()
        self._build_layout()
        self._render_state()

    def _configure_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("Connector.TFrame", background="#f6f7f9")
        self.style.configure(
            "Title.TLabel",
            background="#f6f7f9",
            foreground="#1f2937",
            font=("Segoe UI", 18, "bold"),
        )
        self.style.configure(
            "FieldLabel.TLabel",
            background="#f6f7f9",
            foreground="#4b5563",
            font=("Segoe UI", 10, "bold"),
        )
        self.style.configure(
            "Value.TLabel",
            background="#f6f7f9",
            foreground="#111827",
            font=("Segoe UI", 11),
        )
        self.style.configure(
            "Connect.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(28, 10),
        )

    def _build_layout(self):
        shell = ttk.Frame(self, style="Connector.TFrame", padding=(42, 32))
        shell.pack(fill="both", expand=True)

        title = ttk.Label(shell, text="ZYGN CONNECTOR", style="Title.TLabel")
        title.pack(anchor="center", pady=(0, 26))

        content = ttk.Frame(shell, style="Connector.TFrame")
        content.pack(fill="x")

        self._add_label(content, "Status")
        self.status_label = ttk.Label(content, style="Value.TLabel")
        self.status_label.pack(anchor="w", pady=(4, 18))

        self._add_label(content, "Cloud")
        cloud_value = ttk.Label(content, text=CLOUD_URL, style="Value.TLabel")
        cloud_value.pack(anchor="w", pady=(4, 18))

        self._add_label(content, "Local")
        local_value = ttk.Label(content, text=LOCAL_URL, style="Value.TLabel")
        local_value.pack(anchor="w", pady=(4, 28))

        self.action_button = ttk.Button(
            shell,
            style="Connect.TButton",
            command=self._handle_action,
        )
        self.action_button.pack(anchor="center")

    def _add_label(self, parent, text):
        label = ttk.Label(parent, text=text, style="FieldLabel.TLabel")
        label.pack(anchor="w")

    def _handle_action(self):
        if self.status == STATUS_CONNECTED:
            self._disconnect_websocket()
            return

        if self.status in (STATUS_CONNECTING, STATUS_AUTHENTICATING):
            return

        self._connect_websocket()

    def _connect_websocket(self):
        self.status = STATUS_CONNECTING
        self.last_error = None
        self._render_state()

        self.websocket_client = ZygnWebSocketClient(
            WEBSOCKET_URL,
            self.auth_session.access_token,
            self.auth_session.employee_id,
            on_open=lambda: self._run_on_ui_thread(self._mark_authenticating),
            on_identified=lambda: self._run_on_ui_thread(self._mark_connected),
            on_close=lambda: self._run_on_ui_thread(self._mark_disconnected),
            on_error=lambda error: self._run_on_ui_thread(
                lambda: self._mark_error(error)
            ),
        )
        self.websocket_client.connect()

    def _disconnect_websocket(self):
        if self.websocket_client:
            self.websocket_client.disconnect()

        self.status = STATUS_DISCONNECTED
        self._render_state()

    def _handle_window_close(self):
        if self.websocket_client:
            self.websocket_client.disconnect()

        self.destroy()

    def _mark_authenticating(self):
        self.status = STATUS_AUTHENTICATING
        self._render_state()

    def _mark_connected(self):
        self.status = STATUS_CONNECTED
        self._render_state()

    def _mark_disconnected(self):
        if self.status == STATUS_ERROR:
            return

        self.status = STATUS_DISCONNECTED
        self._render_state()

    def _mark_error(self, error):
        self.status = STATUS_ERROR
        self.last_error = error
        self._render_state()

    def _run_on_ui_thread(self, callback):
        self.after(0, callback)

    def _render_state(self):
        if self.status == STATUS_CONNECTED:
            self.status_label.configure(
                text=f"{STATUS_DOT} Connected", foreground="#15803d"
            )
            self.action_button.configure(text="Disconnect", state="normal")
        elif self.status == STATUS_CONNECTING:
            self.status_label.configure(
                text=f"{STATUS_DOT} Connecting...", foreground="#b45309"
            )
            self.action_button.configure(text="Connect", state="disabled")
        elif self.status == STATUS_AUTHENTICATING:
            self.status_label.configure(
                text=f"{STATUS_DOT} Authenticating...", foreground="#b45309"
            )
            self.action_button.configure(text="Connect", state="disabled")
        elif self.status == STATUS_ERROR:
            self.status_label.configure(
                text=f"{STATUS_DOT} Error: {self.last_error}", foreground="#dc2626"
            )
            self.action_button.configure(text="Connect", state="normal")
        else:
            self.status_label.configure(
                text=f"{STATUS_DOT} Disconnected", foreground="#dc2626"
            )
            self.action_button.configure(text="Connect", state="normal")
