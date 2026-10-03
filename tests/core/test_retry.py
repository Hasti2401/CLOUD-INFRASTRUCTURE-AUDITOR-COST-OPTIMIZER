import pytest

from cloud_auditor.core.retry import retry


def test_retry_returns_successful_result():
    result = retry(
        lambda: "success",
        base_delay=0,
    )

    assert result == "success"


def test_retry_retries_failed_operation():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1

        if attempts < 3:
            raise RuntimeError("temporary failure")

        return "success"

    result = retry(
        operation,
        max_attempts=3,
        base_delay=0,
    )

    assert result == "success"
    assert attempts == 3


def test_retry_raises_after_max_attempts():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("permanent failure")

    with pytest.raises(RuntimeError, match="permanent failure"):
        retry(
            operation,
            max_attempts=3,
            base_delay=0,
        )

    assert attempts == 3


def test_retry_rejects_invalid_max_attempts():
    with pytest.raises(ValueError, match="max_attempts"):
        retry(
            lambda: "success",
            max_attempts=0,
        )


def test_retry_rejects_negative_base_delay():
    with pytest.raises(ValueError, match="base_delay"):
        retry(
            lambda: "success",
            base_delay=-1,
        )


def test_retry_does_not_retry_non_retryable_exception():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise ValueError("not retryable")

    with pytest.raises(ValueError, match="not retryable"):
        retry(
            operation,
            max_attempts=3,
            base_delay=0,
            retryable_exceptions=(RuntimeError,),
        )

    assert attempts == 1