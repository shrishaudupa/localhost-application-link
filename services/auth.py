from dataclasses import dataclass
import base64
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import API_BASE_URL


@dataclass
class AuthSession:
    access_token: str
    employee_id: int
    user: dict


class AuthService:
    def login(self, email, password):
        payload = json.dumps(
            {
                "email": email,
                "password": password,
                "visitorId": "f568a0e9c5a2f0web7234c",
                "browserName": "Chrome",
                "ipAddress": "203.0.113.42",
                "os": "Windows 10",
            }
        ).encode("utf-8")
        request = Request(
            f"{API_BASE_URL.rstrip('/')}/api/users/login",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=20) as response:
                response_body = response.read().decode("utf-8")
        except HTTPError as error:
            message = self._read_error_message(error)
            raise ValueError(message) from error
        except URLError as error:
            raise ValueError(f"Login request failed: {error.reason}") from error

        try:
            data = json.loads(response_body)
        except json.JSONDecodeError as error:
            raise ValueError("Login response was not valid JSON") from error

        token = self._find_first(data, ("accessToken", "access_token", "token", "jwt"))
        if not token:
            raise ValueError("Login response did not include an access token")

        employee_id = self._find_first(
            data,
            ("employeeId", "employee_id", "id"),
            prefer_nested_keys=("employee", "user"),
        )
        if employee_id is None:
            employee_id = self._employee_id_from_token(token)

        if employee_id is None:
            raise ValueError("Login response did not include an employee id")

        return AuthSession(
            access_token=token,
            employee_id=int(employee_id),
            user=data if isinstance(data, dict) else {},
        )

    def _read_error_message(self, error):
        try:
            body = error.read().decode("utf-8")
            data = json.loads(body)
            return (
                data.get("message")
                or data.get("error")
                or f"Login failed with status {error.code}"
            )
        except Exception:
            return f"Login failed with status {error.code}"

    def _find_first(self, value, keys, prefer_nested_keys=()):
        if isinstance(value, dict):
            for nested_key in prefer_nested_keys:
                if nested_key in value:
                    found = self._find_first(value[nested_key], keys, prefer_nested_keys)
                    if found is not None:
                        return found

            for key in keys:
                if key in value and value[key] not in (None, ""):
                    return value[key]

            for item in value.values():
                found = self._find_first(item, keys, prefer_nested_keys)
                if found is not None:
                    return found

        if isinstance(value, list):
            for item in value:
                found = self._find_first(item, keys, prefer_nested_keys)
                if found is not None:
                    return found

        return None

    def _employee_id_from_token(self, token):
        try:
            payload = token.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            decoded_payload = json.loads(base64.urlsafe_b64decode(payload))
        except Exception:
            return None

        return self._find_first(
            decoded_payload,
            ("employeeId", "employee_id", "id"),
            prefer_nested_keys=("user", "employee"),
        )
