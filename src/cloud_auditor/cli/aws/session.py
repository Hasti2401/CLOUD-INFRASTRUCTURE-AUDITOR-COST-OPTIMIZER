"""Reusable AWS session and client utilities."""

import boto3


def create_session(
    profile_name: str = "cloud-auditor",
    region_name: str = "ap-south-1",
) -> boto3.Session:
    """Create and return a reusable Boto3 session.

    Args:
        profile_name: AWS CLI profile to use.
        region_name: Default AWS region for the session.

    Returns:
        A configured boto3 Session.
    """
    return boto3.Session(
        profile_name=profile_name,
        region_name=region_name,
    )


def get_client(
    service_name: str,
    session: boto3.Session,
):
    """Create an AWS service client from an existing session.

    Args:
        service_name: AWS service name, such as 's3', 'ec2', or 'sts'.
        session: Existing boto3 Session.

    Returns:
        A boto3 service client.
    """
    return session.client(service_name)


def get_regions(
    service_name: str = "ec2",
    session: boto3.Session | None = None,
) -> list[str]:
    """Return the AWS regions supported by an AWS service.

    Args:
        service_name: AWS service used to retrieve the region list.
        session: Optional existing boto3 Session.

    Returns:
        A list of AWS region names.
    """
    if session is None:
        session = create_session()

    return session.get_available_regions(service_name)