import threading
import tkinter as tk
from tkinter import ttk

from services.auth import AuthService


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.auth_session = None
        self.auth_service = AuthService()

        self.title("ZYGN CONNECTOR - Login")
        self.geometry("420x360")
        self.minsize(360, 320)
        self.resizable(False, False)
        self.configure(bg="#f6f7f9")

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("Login.TFrame", background="#f6f7f9")
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
            "Error.TLabel",
            background="#f6f7f9",
            foreground="#dc2626",
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Login.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(28, 10),
        )

    def _build_layout(self):
        shell = ttk.Frame(self, style="Login.TFrame", padding=(42, 32))
        shell.pack(fill="both", expand=True)

        title = ttk.Label(shell, text="ZYGN CONNECTOR", style="Title.TLabel")
        title.pack(anchor="center", pady=(0, 26))

        self._add_label(shell, "Email")
        self.email_entry = ttk.Entry(shell, font=("Segoe UI", 11))
        self.email_entry.pack(fill="x", pady=(4, 16), ipady=5)
        self.email_entry.insert(0, "shrisha@gmail.com")

        self._add_label(shell, "Password")
        self.password_entry = ttk.Entry(shell, font=("Segoe UI", 11), show="*")
        self.password_entry.pack(fill="x", pady=(4, 18), ipady=5)
        self.password_entry.insert(0, "pwd@123")

        self.error_label = ttk.Label(shell, text="", style="Error.TLabel", wraplength=330)
        self.error_label.pack(fill="x", pady=(0, 18))

        self.login_button = ttk.Button(
            shell,
            text="Login",
            style="Login.TButton",
            command=self._handle_login,
        )
        self.login_button.pack(anchor="center")

        self.bind("<Return>", lambda _event: self._handle_login())
        self.email_entry.focus_set()

    def _add_label(self, parent, text):
        label = ttk.Label(parent, text=text, style="FieldLabel.TLabel")
        label.pack(anchor="w")

    def _handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self._show_error("Enter email and password")
            return

        self._set_loading(True)
        threading.Thread(
            target=self._login_in_background,
            args=(email, password),
            daemon=True,
        ).start()

    def _login_in_background(self, email, password):
        try:
            session = self.auth_service.login(email, password)
        except Exception as error:
            self.after(0, lambda: self._handle_login_error(str(error)))
            return

        self.after(0, lambda: self._handle_login_success(session))

    def _handle_login_success(self, session):
        self.auth_session = session
        self.destroy()

    def _handle_login_error(self, message):
        self._set_loading(False)
        self._show_error(message)

    def _set_loading(self, is_loading):
        state = "disabled" if is_loading else "normal"
        self.login_button.configure(
            text="Logging in..." if is_loading else "Login",
            state=state,
        )
        self.email_entry.configure(state=state)
        self.password_entry.configure(state=state)
        if is_loading:
            self._show_error("")

    def _show_error(self, message):
        self.error_label.configure(text=message)
