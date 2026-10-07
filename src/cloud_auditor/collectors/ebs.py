"""AWS EBS volume collector."""

from collections.abc import Callable
from typing import Any

from cloud_auditor.cli.aws.retry import retry_aws_operation
from cloud_auditor.models.ebs import EBSVolume


class EBSScanner:
    """Scan AWS for unattached EBS volumes."""

    def __init__(
        self,
        ec2_client: Any,
        retry_operation: Callable[..., Any] = retry_aws_operation,
    ) -> None:
        """Initialize the EBS scanner.

        Args:
            ec2_client: Boto3 EC2 client.
            retry_operation: Retry wrapper used for AWS operations.
        """
        self.ec2_client = ec2_client
        self.retry_operation = retry_operation

    def scan_unattached_volumes(self) -> list[EBSVolume]:
        """Return all unattached EBS volumes.

        AWS represents an unattached EBS volume with the state
        'available'.
        """

        response = self.retry_operation(
            operation=lambda: self.ec2_client.describe_volumes(
                Filters=[
                    {
                        "Name": "status",
                        "Values": ["available"],
                    }
                ]
            )
        )

        volumes = response.get("Volumes", [])

        return [
            self._to_model(volume)
            for volume in volumes
        ]

    @staticmethod
    def _to_model(volume: dict[str, Any]) -> EBSVolume:
        """Convert an AWS EBS volume response into EBSVolume."""

        tags = {
            tag["Key"]: tag["Value"]
            for tag in volume.get("Tags", [])
            if "Key" in tag and "Value" in tag
        }

        return EBSVolume(
            volume_id=volume["VolumeId"],
            availability_zone=volume["AvailabilityZone"],
            volume_type=volume["VolumeType"],
            size_gib=volume["Size"],
            state=volume["State"],
            iops=volume.get("Iops"),
            throughput=volume.get("Throughput"),
            encrypted=volume.get("Encrypted", False),
            snapshot_id=volume.get("SnapshotId"),
            create_time=volume["CreateTime"],
            tags=tags,
        )

def scan_ebs_volumes(
    profile_name: str = "cloud-auditor",
    region_name: str = "ap-south-1",
) -> list[EBSVolume]:
    """Create an EC2 client and scan for unattached EBS volumes."""

    from cloud_auditor.cli.aws.session import create_session, get_client

    session = create_session(
        profile_name=profile_name,
        region_name=region_name,
    )

    ec2_client = get_client("ec2", session)

    scanner = EBSScanner(ec2_client)

    return scanner.scan_unattached_volumes()