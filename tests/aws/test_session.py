from unittest.mock import Mock, patch

from cloud_auditor.cli.aws.session import (
    create_session,
    get_client,
    get_regions,
)

from cloud_auditor.cli.aws.session import create_aws_config

def test_create_session():
    with patch("cloud_auditor.cli.aws.session.boto3.Session") as mock_session:
        session = create_session(
            profile_name="cloud-auditor",
            region_name="ap-south-1",
        )

        mock_session.assert_called_once_with(
            profile_name="cloud-auditor",
            region_name="ap-south-1",
        )

        assert session == mock_session.return_value


def test_get_client():
    mock_session = Mock()
    mock_client = Mock()

    mock_session.client.return_value = mock_client

    client = get_client("s3", mock_session)

    mock_session.client.assert_called_once_with("s3")
    assert client == mock_client


def test_get_regions():
    mock_session = Mock()

    expected_regions = [
        "ap-south-1",
        "ap-southeast-1",
        "us-east-1",
    ]

    mock_session.get_available_regions.return_value = expected_regions

    regions = get_regions("ec2", mock_session)

    mock_session.get_available_regions.assert_called_once_with("ec2")
    assert regions == expected_regions


def test_get_regions_creates_session_when_none_is_provided():
    mock_session = Mock()

    with patch(
        "cloud_auditor.cli.aws.session.create_session",
        return_value=mock_session,
    ):
        mock_session.get_available_regions.return_value = ["ap-south-1"]

        regions = get_regions("ec2")

        mock_session.get_available_regions.assert_called_once_with("ec2")
        assert regions == ["ap-south-1"]


def test_default_aws_timeouts():
    config = create_aws_config()

    assert config.connect_timeout == 10
    assert config.read_timeout == 30


def test_custom_aws_timeouts():
    config = create_aws_config(
        connect_timeout=5,
        read_timeout=15,
    )

    assert config.connect_timeout == 5
    assert config.read_timeout == 15