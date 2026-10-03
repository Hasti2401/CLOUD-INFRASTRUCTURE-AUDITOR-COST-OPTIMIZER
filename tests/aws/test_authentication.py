from unittest.mock import Mock

from cloud_auditor.cli.aws.authentication import verify_aws_authentication
from cloud_auditor.cli.aws.session import create_session


def test_aws_authentication():
    session = create_session()

    mock_sts_client = Mock()
    mock_sts_client.get_caller_identity.return_value = {
        "Account": "123456789012",
        "Arn": "arn:aws:iam::123456789012:user/test-user",
        "UserId": "AIDATESTUSER",
    }

    session.client = Mock(return_value=mock_sts_client)

    identity = verify_aws_authentication(session)

    session.client.assert_called_once_with("sts")
    mock_sts_client.get_caller_identity.assert_called_once_with()

    assert "Account" in identity
    assert "Arn" in identity
    assert "UserId" in identity