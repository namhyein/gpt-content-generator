import logging
import traceback

from package.tools.aws import send_slack

from .base import ValidateError

logger = logging.getLogger(__name__)


HANDLING_ERRORS = [
    TypeError,
    ValueError,
    AttributeError,
    ValidateError,
    Exception
]


def handle_error(e):
    if isinstance(e, Exception):
        logging.error("Unhandled Exception: %s", str(e))

    error_log = {
        "message": str(e),
        "traceback": traceback.format_exc(),
    }

    send_slack(error_log)
    return error_log
