from datetime import datetime, timezone
from unittest.mock import Mock

from cloud_auditor.collectors.ebs import EBSScanner

from unittest.mock import Mock, patch

from cloud_auditor.collectors.ebs import scan_ebs_volumes

def create_volume(
    volume_id: str = "vol-1234567890",
    size: int = 100,
) -> dict:
    """Create a mock AWS EBS volume response."""

    return {
        "VolumeId": volume_id,
        "AvailabilityZone": "ap-south-1a",
        "VolumeType": "gp3",
        "Size": size,
        "State": "available",
        "Iops": 3000,
        "Throughput": 125,
        "Encrypted": True,
        "SnapshotId": "snap-1234567890",
        "CreateTime": datetime(2026, 10, 7, tzinfo=timezone.utc),
        "Tags": [
            {
                "Key": "Environment",
                "Value": "Development",
            },
            {
                "Key": "Project",
                "Value": "CloudAuditor",
            },
        ],
    }


def test_scan_unattached_volumes_returns_volumes():
    """Test that unattached EBS volumes are collected."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [create_volume()]
    }

    scanner = EBSScanner(ec2_client)

    volumes = scanner.scan_unattached_volumes()

    assert len(volumes) == 1
    assert volumes[0].volume_id == "vol-1234567890"
    assert volumes[0].state == "available"


def test_scan_unattached_volumes_returns_multiple_volumes():
    """Test collection of multiple unattached volumes."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [
            create_volume("vol-1111111111", 50),
            create_volume("vol-2222222222", 200),
        ]
    }

    scanner = EBSScanner(ec2_client)

    volumes = scanner.scan_unattached_volumes()

    assert len(volumes) == 2
    assert volumes[0].volume_id == "vol-1111111111"
    assert volumes[0].size_gib == 50
    assert volumes[1].volume_id == "vol-2222222222"
    assert volumes[1].size_gib == 200


def test_scan_unattached_volumes_returns_empty_list():
    """Test behavior when no unattached volumes exist."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": []
    }

    scanner = EBSScanner(ec2_client)

    volumes = scanner.scan_unattached_volumes()

    assert volumes == []


def test_scan_unattached_volumes_uses_available_filter():
    """Test that only unattached EBS volumes are requested from AWS."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [create_volume()]
    }

    scanner = EBSScanner(ec2_client)

    scanner.scan_unattached_volumes()

    ec2_client.describe_volumes.assert_called_once_with(
        Filters=[
            {
                "Name": "status",
                "Values": ["available"],
            }
        ]
    )


def test_ebs_metadata_is_mapped_correctly():
    """Test conversion of AWS metadata into EBSVolume."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [create_volume()]
    }

    scanner = EBSScanner(ec2_client)

    volume = scanner.scan_unattached_volumes()[0]

    assert volume.availability_zone == "ap-south-1a"
    assert volume.volume_type == "gp3"
    assert volume.size_gib == 100
    assert volume.iops == 3000
    assert volume.throughput == 125
    assert volume.encrypted is True
    assert volume.snapshot_id == "snap-1234567890"


def test_ebs_tags_are_converted_to_dictionary():
    """Test conversion of AWS tags into a dictionary."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [create_volume()]
    }

    scanner = EBSScanner(ec2_client)

    volume = scanner.scan_unattached_volumes()[0]

    assert volume.tags == {
        "Environment": "Development",
        "Project": "CloudAuditor",
    }


def test_retry_operation_is_used():
    """Test that the existing AWS retry utility is used."""

    ec2_client = Mock()
    ec2_client.describe_volumes.return_value = {
        "Volumes": [create_volume()]
    }

    retry_operation = Mock(
        return_value={
            "Volumes": [create_volume()]
        }
    )

    scanner = EBSScanner(
        ec2_client,
        retry_operation=retry_operation,
    )

    volumes = scanner.scan_unattached_volumes()

    retry_operation.assert_called_once()
    assert len(volumes) == 1
    assert volumes[0].volume_id == "vol-1234567890"

def test_scan_ebs_volumes_uses_existing_aws_session_utilities():
    """Test integration with the existing AWS session utilities."""

    mock_session = Mock()
    mock_ec2_client = Mock()

    mock_ec2_client.describe_volumes.return_value = {
        "Volumes": []
    }

    with patch(
        "cloud_auditor.cli.aws.session.create_session",
        return_value=mock_session,
    ) as mock_create_session, patch(
        "cloud_auditor.cli.aws.session.get_client",
        return_value=mock_ec2_client,
    ) as mock_get_client:

        volumes = scan_ebs_volumes(
            profile_name="cloud-auditor",
            region_name="ap-south-1",
        )

    mock_create_session.assert_called_once_with(
        profile_name="cloud-auditor",
        region_name="ap-south-1",
    )

    mock_get_client.assert_called_once_with(
        "ec2",
        mock_session,
    )

    assert volumes == []