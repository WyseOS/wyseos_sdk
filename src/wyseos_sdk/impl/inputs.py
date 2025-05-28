from urllib.parse import urlparse

from wyseos_sdk.types.errors import InvalidInputLength, InvalidTimeout, InvalidURL

MIN_TIMEOUT_S = 2  # 2 sec
MAX_TIMEOUT_S = 1800  # 30 mins

MAX_PROMPT_LENGTH = 10000
MIN_PROMPT_LENGTH = 1

MIN_SCREEN_SIZE = 600
MAX_SCREEN_SIZE = 10000


def validate_url(url: str, state: str) -> None:
    """Validate the url value.

    Parameters
    ----------
    url: str
        The url to validate.

    Returns
    -------
    None
    """
    if not isinstance(url, str):
        raise InvalidURL(f"{state} URL provided is not a string.")

    result = urlparse(url)
    if result.scheme != "file" and not all([result.scheme, result.netloc]):
        raise InvalidURL(
            f"{state} URL provided is invalid. Did you include http:// or https:// ?"
        )


def validate_timeout(timeout: int | None) -> None:
    """Validate the timeout value.

    Parameters
    ----------
    timeout: int | None
        The timeout value to validate.

    Returns
    -------
    None
    """
    if timeout is None:
        return
    if not isinstance(timeout, int):
        raise InvalidTimeout("Timeout must be an integer.")
    if timeout < MIN_TIMEOUT_S or timeout > MAX_TIMEOUT_S:
        raise InvalidTimeout(
            f"Timeout must be between {MIN_TIMEOUT_S} and {MAX_TIMEOUT_S}"
        )


def validate_prompt(prompt: str) -> None:
    """Validate the user prompt.

    Parameters
    ----------
    prompt: str
        The user prompt to validate.

    Returns
    -------
    None
    """
    if not isinstance(prompt, str):
        raise InvalidInputLength("Prompt must be a string.")

    if not (MIN_PROMPT_LENGTH <= len(prompt) <= MAX_PROMPT_LENGTH):
        raise InvalidInputLength(
            f"Prompt length must be between 1 and 10000 characters inclusive. Current length: {len(prompt)}"
        )
