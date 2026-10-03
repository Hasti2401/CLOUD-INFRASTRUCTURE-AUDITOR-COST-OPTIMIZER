from cloud_auditor.cli.aws.exceptions import (
    AWSAuthenticationError,
    AWSRequestError,
    AWSThrottlingError,
    CloudAuditorError,
)


def test_aws_authentication_error_is_cloud_auditor_error():
    error = AWSAuthenticationError("Authentication failed")

    assert isinstance(error, CloudAuditorError)


def test_aws_throttling_error_is_cloud_auditor_error():
    error = AWSThrottlingError("Request throttled")

    assert isinstance(error, CloudAuditorError)


def test_aws_request_error_is_cloud_auditor_error():
    error = AWSRequestError("AWS request failed")

    assert isinstance(error, CloudAuditorError)