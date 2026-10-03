"""Reusable AWS session and client utilities."""

import boto3
import logging
from collections.abc import Callable
from typing import TypeVar

from botocore.config import Config

from cloud_auditor.cli.aws.retry import retry_aws_operation

logger = logging.getLogger(__name__)

T = TypeVar("T")

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


def create_aws_config(
    connect_timeout: int = 10,
    read_timeout: int = 30,
) -> Config:
    """Create the Boto3 configuration used by AWS clients."""

    return Config(
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
    )


def execute_aws_operation(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    """
    Execute an AWS operation with retry and error handling.

    Retryable AWS throttling errors are retried using
    exponential backoff.
    """

    logger.debug("Executing AWS operation")

    return retry_aws_operation(
        operation=operation,
        max_attempts=max_attempts,
        base_delay=base_delay,
    )