from enum import IntEnum

class E2eScriptFailure(UserWarning):
    """Simply used to indicate a CI script failure"""

    pass

class E2eExitCodes(IntEnum):
    """Exitcodes
    Note these should not clash with pytest exitcodes: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    """
    CI_SCRIPT_FAILURE = 100
    INVALID_CLIENT_VS_SERVER = 101
    OK = 0
