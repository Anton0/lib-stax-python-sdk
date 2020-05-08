import logging
from json.decoder import JSONDecodeError


class ApiException(Exception):
    def __init__(self, message, response, detail=""):
        try:
            if response.json().get("Error"):
                logging.error(f"{response.status_code}: {response.json()}")
                self.message = f"Api Exception: {response.status_code} -{detail} {response.json()['Error']}"
            else:
                logging.error(f"{response.status_code}: {response.json()}")
                self.message = f"Api Exception:{detail} {message}"
        except JSONDecodeError:
            if response.content:
                logging.error(f"{response.status_code}: {response.content}")
            else:
                logging.error(f"{response.status_code}: {message}")
            self.message = f"Api Exception:{detail} {message}"

    def __str__(self):
        return self.message


class ValidationException(Exception):
    def __init__(self, message):
        # logging.info(f"VALIDATE: {message}")
        self.message = message
