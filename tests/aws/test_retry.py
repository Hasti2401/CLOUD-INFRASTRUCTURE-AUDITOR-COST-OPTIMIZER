import pytest
from botocore.exceptions import ClientError

from cloud_auditor.cli.aws.exceptions import AWSThrottlingError
from cloud_auditor.cli.aws.retry import (
    is_retryable_aws_error,
    retry_aws_operation,
)


def create_client_error(error_code: str) -> ClientError:
    return ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": "Test AWS error",
            }
        },
        "DescribeInstances",
    )


@pytest.mark.parametrize(
    "error_code",
    [
        "Throttling",
        "ThrottlingException",
        "RequestLimitExceeded",
        "TooManyRequestsException",
    ],
)
def test_throttling_errors_are_retryable(error_code):
    error = create_client_error(error_code)

    assert is_retryable_aws_error(error) is True


def test_access_denied_is_not_retryable():
    error = create_client_error("AccessDenied")

    assert is_retryable_aws_error(error) is False


def test_invalid_credentials_are_not_retryable():
    error = create_client_error("InvalidClientTokenId")

    assert is_retryable_aws_error(error) is False


def test_throttling_eventually_succeeds():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1

        if attempts < 3:
            raise create_client_error("Throttling")

        return "success"

    result = retry_aws_operation(
        operation,
        max_attempts=3,
        base_delay=0,
    )

    assert result == "success"
    assert attempts == 3


def test_throttling_raises_after_max_attempts():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise create_client_error("Throttling")

    with pytest.raises(AWSThrottlingError):
        retry_aws_operation(
            operation,
            max_attempts=3,
            base_delay=0,
        )

    assert attempts == 3


def test_access_denied_is_raised_without_retry():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        raise create_client_error("AccessDenied")

    with pytest.raises(ClientError):
        retry_aws_operation(
            operation,
            max_attempts=3,
            base_delay=0,
        )

    assert attempts == 1