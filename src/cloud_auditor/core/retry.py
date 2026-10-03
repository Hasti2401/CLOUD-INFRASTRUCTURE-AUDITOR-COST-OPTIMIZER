import logging
import time
from collections.abc import Callable
from typing import TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    should_retry: Callable[[Exception], bool] | None = None,
) -> T:
    """
    Execute an operation with retries and exponential backoff.

    Args:
        operation: Function to execute.
        max_attempts: Maximum number of attempts.
        base_delay: Initial delay between retries.
        retryable_exceptions: Exception types that may be retried.
        should_retry: Optional function that determines whether
            a specific exception should be retried.

    Returns:
        The result returned by the operation.

    Raises:
        Exception: The final exception if the operation fails.
        ValueError: If configuration values are invalid.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if base_delay < 0:
        raise ValueError("base_delay cannot be negative")

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()

        except retryable_exceptions as exc:
            if should_retry is not None and not should_retry(exc):
                raise

            if attempt == max_attempts:
                logger.error(
                    "Operation failed after %d attempts: %s",
                    attempt,
                    exc,
                )
                raise

            delay = base_delay * (2 ** (attempt - 1))

            logger.warning(
                "Operation failed on attempt %d/%d. "
                "Retrying in %.2f seconds: %s",
                attempt,
                max_attempts,
                delay,
                exc,
            )

            time.sleep(delay)

    raise RuntimeError("Retry operation exited unexpectedly")