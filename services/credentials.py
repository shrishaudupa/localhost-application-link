import keyring


class CredentialService:

    APP_NAME = "ZygnConnector"

    def save_password(self, email, password):
        keyring.set_password(
            self.APP_NAME,
            email,
            password
        )

    def get_password(self, email):
        return keyring.get_password(
            self.APP_NAME,
            email
        )

    def delete_password(self, email):
        try:
            keyring.delete_password(
                self.APP_NAME,
                email
            )
        except Exception:
            pass