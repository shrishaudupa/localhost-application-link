from ui.login import LoginApp
from ui.dashboard import zygnConnectorApp
from database.database import initialize_database


def main():
    initialize_database()

    login = LoginApp()
    login.mainloop()

    if login.auth_session:
        app = zygnConnectorApp(login.auth_session)
        app.mainloop()


if __name__ == "__main__":
    main()
