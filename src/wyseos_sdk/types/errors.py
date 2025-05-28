from abc import ABC

from wyseos_sdk.util.logging import create_warning_box


class WyseOSError(Exception, ABC):
    """Superclass for all WyseOS SDK exceptions."""


"""
Wrapper classes for unhandled exceptions
"""


class AuthError(WyseOSError):
    """Indicates there's error with user auth"""

    def __init__(
        self,
        *,
        message: str = "Authentication failed.",
        request_id: str = "",
    ):
        warning = create_warning_box(
            [
                message,
                "",
                "Please ensure you are using a key from WyseMate.",
            ]
        )

        if request_id:
            warning += (
                "\nIf the above requirements are satisfied and you are still facing Error, "
                f"please submit an issue with this request ID: {request_id}"
            )
        super().__init__(warning)


class ValidationFailed(WyseOSError, ABC):
    """Indicates assumptions violated about how the SDK can be used"""


class ClientNotStarted(ValidationFailed):
    pass


class InvalidPlaywrightState(WyseOSError):
    pass


class InvalidPageState(WyseOSError):
    pass


class UnsupportedOperatingSystem(ValidationFailed):
    pass


class InvalidInputLength(ValidationFailed):
    pass


class InvalidScreenResolution(ValidationFailed):
    pass


class InvalidPath(ValidationFailed):
    pass


class InvalidURL(ValidationFailed):
    pass


class InvalidCertificate(ValidationFailed):
    pass


class InvalidTimeout(ValidationFailed):
    pass


class InvalidMaxSteps(ValidationFailed):
    def __init__(self, num_steps_allowed: int):
        super().__init__(f"Please choose a number less than {num_steps_allowed}")


class InvalidChromeChannel(ValidationFailed):
    pass


class PageNotFoundError(ValidationFailed):
    pass
