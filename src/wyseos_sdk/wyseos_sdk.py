import os
import tempfile
import uuid

from wyseos_sdk.impl.backend import Backend, get_urls_for_backend
from wyseos_sdk.impl.inputs import validate_timeout
from wyseos_sdk.types.errors import AuthError, ClientNotStarted, StartFailed
from wyseos_sdk.util.logging import (
    make_trace_logger,
    set_logging_session,
    setup_logging,
)

DEFAULT_SCREEN_WIDTH = 1440
DEFAULT_SCREEN_HEIGHT = 900

DEFAULT_MAX_ROUNDS = 30

_LOGGER = setup_logging(__name__)
_TRACE_LOGGER = make_trace_logger()


class WyseOS:
    """Client for interacting with the WyseOS SDK."""

    def __init__(
        self,
        starting_page: str,
        screen_width: int = DEFAULT_SCREEN_WIDTH,
        screen_height: int = DEFAULT_SCREEN_HEIGHT,
        headless: bool = False,
        wyseos_api_key: str | None = None,
        record_video: bool = False,
        go_to_url_timeout: int | None = None,
        logs_directory: str | None = None,
    ):
        """Initialize a sdk object."""
        self._backend = Backend.PROD
        self._backend_info = get_urls_for_backend(self._backend)

        self._starting_page = starting_page or "https://www.google.com"

        if go_to_url_timeout is not None:
            validate_timeout(go_to_url_timeout)
        self.go_to_url_timeout = go_to_url_timeout

        wyseos_api_key = wyseos_api_key or os.environ.get("WYSEOS_API_KEY")
        if not wyseos_api_key:
            raise AuthError()

        if logs_directory is None:
            logs_directory = tempfile.mkdtemp(suffix="wyseos_sdk_logs")

        self._logs_directory = logs_directory

        self.screen_width = screen_width
        self.screen_height = screen_height
        self._session_id: str | None = None

    def get_session_id(self) -> str:
        """Get the session ID for the current client.

        Raises ClientNotStarted if the client has not been started.
        """
        if not self.started:
            raise ClientNotStarted(
                "Client must be started before accessing the session ID."
            )
        return str(self._session_id)

    def get_logs_directory(self) -> str:
        """Get the logs directory for the current client."""
        if not self._logs_directory:
            raise ValueError("Logs directory is not set.")

        return self._logs_directory

    def start(self) -> None:
        """Start the WyseOS SDK."""
        try:
            self._session_id = str(uuid.uuid4())
            set_logging_session(self._session_id)

            if self._logs_directory:
                session_logs_directory = os.path.join(
                    self._logs_directory, self._session_id
                )
            else:
                session_logs_directory = ""

            if session_logs_directory:
                try:
                    os.mkdir(session_logs_directory)
                except Exception as e:
                    _LOGGER.error(
                        f"Failed to create directory: {session_logs_directory} with Error: {e} "
                        f"of type {type(e).__name__}"
                    )

            _TRACE_LOGGER.info(
                f"\nstart session {self._session_id} on {self._starting_page}{self._logs_directory}\n"
            )

        except Exception as e:
            raise StartFailed from e
