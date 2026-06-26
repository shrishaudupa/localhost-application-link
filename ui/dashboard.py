import tkinter as tk
from tkinter import ttk


CLOUD_URL = "https://dev-arivu-frontend.rover.zygn.app/"
LOCAL_URL = "http://localhost:9000"


class zygnConnectorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.connected = False

        self.title("ZYGN CONNECTOR")
        self.geometry("420x360")
        self.minsize(360, 320)
        self.resizable(False, False)
        self.configure(bg="#f6f7f9")

        self._configure_styles()
        self._build_layout()
        self._render_state()

    def _configure_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(
            "Connector.TFrame",
            background="#f6f7f9",
        )
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
            command=self._toggle_connection,
        )
        self.action_button.pack(anchor="center")

    def _add_label(self, parent, text):
        label = ttk.Label(parent, text=text, style="FieldLabel.TLabel")
        label.pack(anchor="w")

    def _toggle_connection(self):
        self.connected = not self.connected
        self._render_state()

    def _render_state(self):
        if self.connected:
            self.status_label.configure(text="● Connected", foreground="#15803d")
            self.action_button.configure(text="Disconnect")
        else:
            self.status_label.configure(text="● Disconnected", foreground="#dc2626")
            self.action_button.configure(text="Connect")
