import logging
import os
import sys
from contextvars import ContextVar

_session_id = ContextVar("session_id", default=None)


def get_session_id_prefix() -> str:
    session_id = _session_id.get()
    if session_id is None:
        session_id = ""
    return f"{session_id[:4]}> "


def set_logging_session(session_id: str | None) -> None:
    _session_id.set(session_id)  # type: ignore


_LOG_ENV_VAR = "WYSEOS_SDK_LOG_LEVEL"


def get_log_level():
    return int(os.environ.get(_LOG_ENV_VAR, logging.INFO))


def is_quiet():
    return get_log_level() > logging.INFO


def setup_logging(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)

    # Add a handler only if it hasn't been already set up.
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(get_log_level())

    return logger


def make_trace_logger() -> logging.Logger:
    logger = logging.Logger("trace", level=get_log_level())
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class LoadScroller:
    """Print horizontal dots until stop condition"""

    def __init__(self, condition_check=lambda: True, frequency: int = 1):
        if frequency < 1:
            raise ValueError("Frequency must be greater than 1")

        self.condition_check = condition_check
        self.toggled = False
        self._frequency = frequency
        self._count = 0

    def scroll(self):
        if not self.condition_check():
            return

        self._count += 1
        if self._count >= self._frequency:
            self._count = 0
            print(".", end="", flush=True, file=sys.stderr)


def create_warning_box(messages: list[str]) -> str:
    # Find the longest line to determine box width
    max_length = max(len(line) for line in messages)
    width = max_length + 4  # 4 accounts for spaces and stars on sides

    # Create box parts
    border = "*" * width
    middle_lines = []
    for msg in messages:
        padding = " " * (width - len(msg) - 4)
        middle_lines.append(f"* {msg}{padding} *")

    # Combine all parts
    return f"\n{border}\n{chr(10).join(middle_lines)}\n{border}"
