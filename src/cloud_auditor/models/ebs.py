"""Pydantic models for AWS EBS resources."""

from datetime import datetime

from pydantic import BaseModel, Field


class EBSVolume(BaseModel):
    """Represent an AWS EBS volume."""

    volume_id: str
    availability_zone: str
    volume_type: str
    size_gib: int
    state: str

    iops: int | None = None
    throughput: int | None = None

    encrypted: bool
    snapshot_id: str | None = None

    create_time: datetime
    tags: dict[str, str] = Field(default_factory=dict)