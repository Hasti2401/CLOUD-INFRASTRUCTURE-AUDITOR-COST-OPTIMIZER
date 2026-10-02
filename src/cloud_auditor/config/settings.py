"""AWS configuration settings."""

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass
class AWSSettings:
    """Configuration settings required for AWS access."""

    account_id: str | None = None
    profile: str = "default"
    region: str = "ap-south-1"

    def __post_init__(self) -> None:
        """Validate AWS configuration values."""

        if self.account_id is not None:
            if not self.account_id.isdigit() or len(self.account_id) != 12:
                raise ValueError(
                    "AWS account ID must contain exactly 12 digits."
                )

        if not self.profile.strip():
            raise ValueError(
                "AWS profile cannot be empty."
            )

        if not self.region.strip():
            raise ValueError(
                "AWS region cannot be empty."
            )


def load_yaml_config(config_path: str | Path) -> AWSSettings:
    """Load AWS settings from a YAML configuration file."""

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    aws_config = config.get("aws", {})

    return AWSSettings(
        account_id=aws_config.get("account_id") or None,
        profile=aws_config.get("profile", "default"),
        region=aws_config.get("region", "ap-south-1"),
    )


def load_environment_config(
    load_dotenv_file: bool = True,
) -> dict[str, str | None]:
    """Load AWS configuration values from environment variables."""

    if load_dotenv_file:
        load_dotenv()

    return {
        "account_id": os.getenv("AWS_ACCOUNT_ID") or None,
        "profile": os.getenv("AWS_PROFILE"),
        "region": os.getenv("AWS_DEFAULT_REGION"),
    }

def load_settings(
    config_path: str | Path,
    load_dotenv_file: bool = True,
) -> AWSSettings:
    """Load AWS settings using environment variables, YAML, and defaults."""

    yaml_settings = load_yaml_config(config_path)
    env_settings = load_environment_config(
        load_dotenv_file=load_dotenv_file
    )

    return AWSSettings(
        account_id=(
            env_settings["account_id"]
            if env_settings["account_id"] is not None
            else yaml_settings.account_id
        ),
        profile=(
            env_settings["profile"]
            if env_settings["profile"] is not None
            else yaml_settings.profile
        ),
        region=(
            env_settings["region"]
            if env_settings["region"] is not None
            else yaml_settings.region
        ),
    )