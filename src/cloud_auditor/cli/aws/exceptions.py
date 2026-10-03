class CloudAuditorError(Exception):
    """Base exception for Cloud Auditor."""
    pass


class AWSAuthenticationError(CloudAuditorError):
    """Raised when AWS authentication fails."""
    pass


class AWSThrottlingError(CloudAuditorError):
    """Raised when AWS throttles a request."""
    pass


class AWSRequestError(CloudAuditorError):
    """Raised when an AWS request fails."""
    pass