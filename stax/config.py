import logging
import os

import requests

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("nose").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Config:
    """
    Insert doco here
    """

    STAX_REGION = os.getenv("STAX_REGION", "au1.staxapp.cloud")
    STAX_STAGE = os.getenv("STAX_STAGE", "stax-au1")
    API_VERSION = "20190206"

    api_config = dict()
    access_key = None
    secret_key = None
    auth_class = None
    _initialized = False
    base_url = None
    hostname = f"api.{STAX_REGION}"
    org_id = None
    auth = None
    expiration = None
    load_live_schema = False

    @classmethod
    def set_config(cls):
        if cls.branch() == "master":
            cls.base_url = f"https://api.{cls.STAX_REGION}/{cls.API_VERSION}"
        else:
            cls.base_url = f"https://api.{cls.STAX_STAGE}-{cls.branch()}.{cls.STAX_REGION}/{cls.API_VERSION}"
        config_url = cls.api_base_url() + "/public/config"
        config_response = requests.get(config_url)
        # logging.debug(f"IDAM: get config from {config_url}")
        if(config_response.json().get('Error')):
            raise Exception(f'Could not configure sdk. Error is {config_response.json()["Error"]}')
        cls.api_config = config_response.json()

    @classmethod
    def init(cls, config=None):
        if cls._initialized:
            return

        if not config:
            cls.set_config()

        cls._initialized = True

    @classmethod
    def api_base_url(cls):
        return cls.base_url

    @classmethod
    def branch(cls):
        return os.getenv("STAX_BRANCH", "master")

    @classmethod
    def schema_url(cls):
         f"https://{cls.base_url}/public/api-document"

    @classmethod
    def auth(cls):
        # logging.debug(f"AUTHCLASS: {cls.auth_class}")
        if cls.auth_class is None:
            from stax.auth import ApiTokenAuth

            cls.auth_class = ApiTokenAuth
        return cls.auth_class


Config.init()
