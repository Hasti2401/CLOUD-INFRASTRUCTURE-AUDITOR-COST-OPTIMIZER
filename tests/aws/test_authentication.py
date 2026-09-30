from cloud_auditor.cli.aws.authentication import (
    create_aws_session,
    verify_aws_authentication,
)


def test_aws_authentication():
    session = create_aws_session()

    identity = verify_aws_authentication(session)

    assert "Account" in identity
    assert "Arn" in identity
    assert "UserId" in identity