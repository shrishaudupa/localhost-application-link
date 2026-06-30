import threading
import tkinter as tk
import customtkinter as ctk

from database.database import get_saved_emails, save_email, delete_email
from services.credentials import CredentialService
from services.auth import AuthService

# Set global appearance and color theme
ctk.set_appearance_mode("light")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Using built-in blue as base accent


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.auth_session = None
        self.auth_service = AuthService()
        self.credential_service = CredentialService()

        # Window Settings
        self.title("ZYGN CONNECTOR - Login")
        self.geometry("440x480")
        self.resizable(False, False)
        
        # Color Palette Configuration
        self.bg_color = "#FFFFFF"
        self.text_primary = "#111827"    # Dark slate/gray
        self.text_secondary = "#4B5563"  # Cool gray
        self.accent_color = "#3B82F6"    # Vibrant primary blue
        self.accent_hover = "#2563EB"    # Darker blue for hover state
        self.error_color = "#EF4444"     # Smooth red

        self.configure(fg_color=self.bg_color)
        self._build_layout()

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
        ).pack(anchor="w", pady=(10, 30))

        # --- Email Field ---
        self._add_label(shell, "Email")

        emails = get_saved_emails()

        # CustomTkinter ComboBox acts cleanly and supports rounded corners
        self.email_entry = ctk.CTkComboBox(
            shell,
            values=emails,
            font=("Segoe UI", 13),
            fg_color="#F3F4F6",          # Soft gray fill
            text_color=self.text_primary,
            border_width=0,              # No explicit borders for flat modern look
            corner_radius=8,
            height=42,
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color=self.text_primary,
            command=self._on_email_selected_cb, # Combobox item selection bind
        )
        self.email_entry.pack(fill="x", pady=(6, 20))
        # Direct key entry string handling bind
        self.email_entry._entry.bind("<KeyRelease>", self._on_email_selected) 

        # --- Password Field ---
        self._add_label(shell, "Password")

        self.password_entry = ctk.CTkEntry(
            shell,
            font=("Segoe UI", 13),
            show="*",
            fg_color="#F3F4F6",
            text_color=self.text_primary,
            border_width=0,
            corner_radius=8,
            height=42,
        )
        self.password_entry.pack(fill="x", pady=(6, 16))

        # --- Remember Me Checkbox ---
        self.remember_var = tk.BooleanVar(value=False)

        self.remember_checkbox = ctk.CTkCheckBox(
            shell,
            text="Remember Me",
            variable=self.remember_var,
            text_color=self.text_secondary,
            font=("Segoe UI", 12),
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            border_width=2,
            border_color="#9CA3AF",
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
        )
        self.remember_checkbox.pack(anchor="w", pady=(0, 10))

        # --- Error Information Bar ---
        self.error_label = ctk.CTkLabel(
            shell,
            text="",
            text_color=self.error_color,
            font=("Segoe UI", 12),
            wraplength=350,
            justify="left",
        )
        self.error_label.pack(fill="x", pady=(5, 15), anchor="w")

        # --- Premium Login CTA Button ---
        self.login_button = ctk.CTkButton(
            shell,
            text="Login",
            font=("Segoe UI", 14, "bold"),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            text_color="#FFFFFF",
            height=46,
            corner_radius=8,
            command=self._handle_login,
        )
        self.login_button.pack(fill="x", pady=(10, 0))

        # Global event binds
        self.bind("<Return>", lambda _event: self._handle_login())

        # Pre-populate defaults if history is found
        if emails:
            self.email_entry.set(emails[0])
            self._on_email_selected()

        self.email_entry.focus_set()

    def _add_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=self.text_secondary,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")

    def _handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self._show_error("Please enter both your email and password.")
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
            self.after(0, lambda: self._handle_login_success(session))
        except Exception as error:
            self.after(0, lambda: self._handle_login_error(str(error)))

    def _on_email_selected_cb(self, choice):
        self._on_email_selected()

    def _on_email_selected(self, event=None):
        email = self.email_entry.get().strip()
        password = self.credential_service.get_password(email)

        self.password_entry.delete(0, tk.END)

        if password:
            self.password_entry.insert(0, password)
            self.remember_var.set(True)
        else:
            self.remember_var.set(False)

        self.password_entry.focus()
        self.password_entry._entry.icursor(tk.END)

    def _remember_user(self, email, password):
        if self.remember_var.get():
            save_email(email)
            self.credential_service.save_password(email, password)
        else:
            delete_email(email)
            self.credential_service.delete_password(email)

        self.email_entry.configure(values=get_saved_emails())

    def _handle_login_success(self, session):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        self._remember_user(email, password)
        self.auth_session = session
        self.destroy()

    def _handle_login_error(self, message):
        self._set_loading(False)
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus_set()
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


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()