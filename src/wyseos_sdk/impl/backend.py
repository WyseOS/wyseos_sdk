from dataclasses import dataclass
from enum import Enum


class Backend(Enum):
    PROD = "prod"
    LOCAL = "local"


@dataclass
class BackendInfo:
    api_uri: str
    keygen_uri: str


URLS_BY_BACKEND = {
    Backend.PROD: BackendInfo(
        "https://api.wyseos.com",
    ),
    Backend.LOCAL: BackendInfo(
        "http://localhost:13001",
    ),
}


def get_urls_for_backend(backend: Backend) -> BackendInfo:
    return URLS_BY_BACKEND[backend]
