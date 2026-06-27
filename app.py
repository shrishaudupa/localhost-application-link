from ui.login import LoginApp
from ui.dashboard import zygnConnectorApp


def main():
    login = LoginApp()
    login.mainloop()

    if login.auth_session:
        app = zygnConnectorApp(login.auth_session)
        app.mainloop()


if __name__ == "__main__":
    main()
