"""Tests for AWS configuration settings."""

from pathlib import Path

import pytest

from cloud_auditor.config.settings import (
    AWSSettings,
    load_environment_config,
    load_settings,
    load_yaml_config,
)


def test_load_yaml_config(tmp_path: Path) -> None:
    """Test loading AWS settings from a YAML file."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
aws:
  account_id: "123456789012"
  profile: "cloud-auditor"
  region: "ap-south-1"
""",
        encoding="utf-8",
    )

    settings = load_yaml_config(config_file)

    assert settings.account_id == "123456789012"
    assert settings.profile == "cloud-auditor"
    assert settings.region == "ap-south-1"


def test_load_yaml_config_missing_file(tmp_path: Path) -> None:
    """Test that a missing YAML file raises an error."""

    config_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_yaml_config(config_file)


def test_load_environment_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading AWS configuration from environment variables."""

    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_PROFILE", "cloud-auditor")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-south-1")

    settings = load_environment_config()

    assert settings["account_id"] == "123456789012"
    assert settings["profile"] == "cloud-auditor"
    assert settings["region"] == "ap-south-1"


def test_environment_variables_override_yaml(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that environment variables override YAML configuration."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
aws:
  account_id: "111111111111"
  profile: "yaml-profile"
  region: "us-east-1"
""",
        encoding="utf-8",
    )

    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_PROFILE", "cloud-auditor")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-south-1")

    settings = load_settings(config_file)

    assert settings.account_id == "123456789012"
    assert settings.profile == "cloud-auditor"
    assert settings.region == "ap-south-1"


def test_yaml_used_when_environment_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that YAML values are used when environment variables are absent."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
aws:
  account_id: "123456789012"
  profile: "yaml-profile"
  region: "us-east-1"
""",
        encoding="utf-8",
    )

    monkeypatch.delenv("AWS_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)

    settings = load_settings(config_file, load_dotenv_file=False)

    assert settings.account_id == "123456789012"
    assert settings.profile == "yaml-profile"
    assert settings.region == "us-east-1"


def test_default_values() -> None:
    """Test AWSSettings default values."""

    settings = AWSSettings()

    assert settings.account_id is None
    assert settings.profile == "default"
    assert settings.region == "ap-south-1"


def test_valid_account_id() -> None:
    """Test a valid AWS account ID."""

    settings = AWSSettings(account_id="123456789012")

    assert settings.account_id == "123456789012"


def test_invalid_account_id() -> None:
    """Test that an invalid AWS account ID raises an error."""

    with pytest.raises(
        ValueError,
        match="AWS account ID must contain exactly 12 digits",
    ):
        AWSSettings(account_id="12345")


def test_empty_profile() -> None:
    """Test that an empty AWS profile raises an error."""

    with pytest.raises(
        ValueError,
        match="AWS profile cannot be empty",
    ):
        AWSSettings(profile="")


def test_empty_region() -> None:
    """Test that an empty AWS region raises an error."""

    with pytest.raises(
        ValueError,
        match="AWS region cannot be empty",
    ):
        AWSSettings(region="")


def test_invalid_account_id_with_letters() -> None:
    """Test that an account ID containing letters is rejected."""

    with pytest.raises(
        ValueError,
        match="AWS account ID must contain exactly 12 digits",
    ):
        AWSSettings(account_id="123456789ABC")