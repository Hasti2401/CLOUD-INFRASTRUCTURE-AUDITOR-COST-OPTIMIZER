"""AWS authentication utilities."""

from .session import create_session


def create_aws_session():
    """Create and return the configured AWS session.

    Returns:
        A configured boto3 Session.
    """
    return create_session()


def verify_aws_authentication(session):
    """Verify AWS credentials using STS.

    Args:
        session: Existing boto3 Session.

    Returns:
        AWS caller identity information.
    """
    sts_client = session.client("sts")

    return sts_client.get_caller_identity()