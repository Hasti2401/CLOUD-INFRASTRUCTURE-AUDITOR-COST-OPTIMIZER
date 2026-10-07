from datetime import datetime, timezone

from cloud_auditor.models.ebs import EBSVolume


def test_ebs_volume_model():
    volume = EBSVolume(
        volume_id="vol-1234567890",
        availability_zone="ap-south-1a",
        volume_type="gp3",
        size_gib=100,
        state="available",
        iops=3000,
        throughput=125,
        encrypted=True,
        snapshot_id="snap-1234567890",
        create_time=datetime(2026, 10, 7, tzinfo=timezone.utc),
        tags={"Environment": "Development"},
    )

    assert volume.volume_id == "vol-1234567890"
    assert volume.availability_zone == "ap-south-1a"
    assert volume.volume_type == "gp3"
    assert volume.size_gib == 100
    assert volume.state == "available"
    assert volume.iops == 3000
    assert volume.throughput == 125
    assert volume.encrypted is True
    assert volume.snapshot_id == "snap-1234567890"
    assert volume.tags["Environment"] == "Development"