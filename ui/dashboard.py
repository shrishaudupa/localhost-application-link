import tkinter as tk
import customtkinter as ctk

from config import CLOUD_URL, LOCAL_URL, WEBSOCKET_URL
from tunnel.websocket_client import ZygnWebSocketClient

STATUS_DISCONNECTED = "disconnected"
STATUS_CONNECTING = "connecting"
STATUS_AUTHENTICATING = "authenticating"
STATUS_CONNECTED = "connected"
STATUS_ERROR = "error"
STATUS_DOT = "\u25cf"

# Set global appearance and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class zygnConnectorApp(ctk.CTk):
    def __init__(self, auth_session):
        super().__init__()

        self.auth_session = auth_session
        self.status = STATUS_DISCONNECTED
        self.last_error = None
        self.websocket_client = None

        # Window Settings
        self.title("ZYGN CONNECTOR")
        self.geometry("440x480")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._handle_window_close)

        # Color Palette Configuration (Matching Login Theme)
        self.bg_color = "#FFFFFF"
        self.card_bg = "#F3F4F6"         # Light gray for structuring rows
        self.text_primary = "#111827"    # Dark slate/gray
        self.text_secondary = "#4B5563"  # Cool gray
        self.accent_color = "#3B82F6"    # Primary blue
        self.accent_hover = "#2563EB"    # Darker blue for hover state
        
        # Status Color Profiles
        self.color_success = "#16A34A"   # Green
        self.color_warning = "#D97706"   # Amber/Orange
        self.color_danger = "#DC2626"    # Red

        self.configure(fg_color=self.bg_color)
        self._build_layout()
        self._render_state()

    def _build_layout(self):
        # Container frame for margins and alignment
        shell = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        shell.pack(fill="both", expand=True, padx=40, pady=40)

        # App branding header
        ctk.CTkLabel(
            shell,
            text="ZYGN CONNECTOR",
            text_color=self.text_primary,
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", pady=(10, 24))

        # Main Data Frame (Groups the connections and statuses)
        content = ctk.CTkFrame(shell, fg_color=self.bg_color, corner_radius=0)
        content.pack(fill="x", expand=True)

        # --- Status Block ---
        self._add_label(content, "Status")
        self.status_label = ctk.CTkLabel(
            content,
            text="",
            font=("Segoe UI", 15, "bold"),
            justify="left",
        )
        self.status_label.pack(anchor="w", pady=(4, 20))

        # --- Cloud Endpoint Block ---
        self._add_label(content, "Cloud URL")
        cloud_value = ctk.CTkLabel(
            content,
            text=CLOUD_URL,
            text_color=self.text_primary,
            font=("Segoe UI", 13),
            fg_color=self.card_bg,
            corner_radius=6,
            height=36,
            anchor="w",
        )
        cloud_value.pack(fill="x", pady=(4, 20), ipady=2, padx=2)

        # --- Local Endpoint Block ---
        self._add_label(content, "Local URL")
        local_value = ctk.CTkLabel(
            content,
            text=LOCAL_URL,
            text_color=self.text_primary,
            font=("Segoe UI", 13),
            fg_color=self.card_bg,
            corner_radius=6,
            height=36,
            anchor="w",
        )
        local_value.pack(fill="x", pady=(4, 30), ipady=2, padx=2)

        # --- Premium Full-Width Action Button ---
        self.action_button = ctk.CTkButton(
            shell,
            text="Connect",
            font=("Segoe UI", 14, "bold"),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            text_color="#FFFFFF",
            height=46,
            corner_radius=8,
            command=self._handle_action,
        )
        self.action_button.pack(fill="x", pady=(10, 0))

    def _add_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=self.text_secondary,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")

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
                text=f"{STATUS_DOT} Connected", text_color=self.color_success
            )
            self.action_button.configure(
                text="Disconnect", 
                state="normal",
                fg_color=self.color_danger,
                hover_color="#B91C1C" # Darker red for disconnect hover
            )
        elif self.status == STATUS_CONNECTING:
            self.status_label.configure(
                text=f"{STATUS_DOT} Connecting...", text_color=self.color_warning
            )
            self.action_button.configure(
                text="Connecting...", 
                state="disabled",
                fg_color=self.accent_color
            )
        elif self.status == STATUS_AUTHENTICATING:
            self.status_label.configure(
                text=f"{STATUS_DOT} Authenticating...", text_color=self.color_warning
            )
            self.action_button.configure(
                text="Authenticating...", 
                state="disabled",
                fg_color=self.accent_color
            )
        elif self.status == STATUS_ERROR:
            self.status_label.configure(
                text=f"{STATUS_DOT} Error: {self.last_error}", text_color=self.color_danger
            )
            self.action_button.configure(
                text="Connect", 
                state="normal",
                fg_color=self.accent_color,
                hover_color=self.accent_hover
            )
        else:
            self.status_label.configure(
                text=f"{STATUS_DOT} Disconnected", text_color=self.color_danger
            )
            self.action_button.configure(
                text="Connect", 
                state="normal",
                fg_color=self.accent_color,
                hover_color=self.accent_hover
            )


if __name__ == "__main__":
    # Dummy session runner logic for isolated testing
    class DummySession:
        access_token = "mock_token"
        employee_id = "mock_id"
        
    app = zygnConnectorApp(DummySession())
    app.mainloop()