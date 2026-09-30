import boto3


def create_aws_session(
    profile_name: str = "cloud-auditor",
    region_name: str = "ap-south-1",
):
    return boto3.Session(
        profile_name=profile_name,
        region_name=region_name,
    )


def verify_aws_authentication(session):
    sts_client = session.client("sts")

    return sts_client.get_caller_identity()