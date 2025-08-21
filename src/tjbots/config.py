from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PackageConfig(BaseSettings):
    """
    Configuration and control plane for the TJBots Package
    """

    openai_api_key: Optional[SecretStr] = Field(alias="OPENAI_API_KEY", default=None)
    google_api_key: Optional[SecretStr] = Field(alias="GOOGLE_API_KEY", default=None)
    anthropic_api_key: Optional[SecretStr] = Field(
        alias="ANTHROPIC_API_KEY", default=None
    )

    model_config = SettingsConfigDict(
        env_file="/run/secrets/tjbots.env",
        extra="ignore",
    )
