import logging
from collections.abc import Callable
from typing import TypeVar

from botocore.exceptions import ClientError

from cloud_auditor.cli.aws.exceptions import AWSThrottlingError
from cloud_auditor.core.retry import retry


logger = logging.getLogger(__name__)

T = TypeVar("T")


RETRYABLE_AWS_ERROR_CODES = {
    "Throttling",
    "ThrottlingException",
    "RequestLimitExceeded",
    "TooManyRequestsException",
}


def is_retryable_aws_error(exc: Exception) -> bool:
    """Return True when an AWS exception should be retried."""

    if not isinstance(exc, ClientError):
        return False

    error_code = exc.response.get("Error", {}).get("Code")

    return error_code in RETRYABLE_AWS_ERROR_CODES


def retry_aws_operation(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Execute an AWS operation with throttling retry handling."""

    try:
        return retry(
            operation=operation,
            max_attempts=max_attempts,
            base_delay=base_delay,
            retryable_exceptions=(ClientError,),
            should_retry=is_retryable_aws_error,
        )

    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")

        if is_retryable_aws_error(exc):
            logger.error(
                "AWS throttling error after maximum retries: %s",
                error_code,
            )

            raise AWSThrottlingError(
                f"AWS request was throttled: {error_code}"
            ) from exc

        raise