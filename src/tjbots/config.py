import os

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PackageConfig(BaseSettings):
    """
    Configuration and control plane for the TJBots Package
    """

    openai_api_key: SecretStr | None = Field(alias="OPENAI_API_KEY", default=None)
    google_api_key: SecretStr | None = Field(alias="GOOGLE_API_KEY", default=None)
    anthropic_api_key: SecretStr | None = Field(alias="ANTHROPIC_API_KEY", default=None)

    model_config = SettingsConfigDict(
        env_file=os.getenv("TJBOTS_ENV_FILE", "/run/secrets/tjbots.env"),
        extra="ignore",
    )

    @model_validator(mode="after")
    def setup_environment(self):
        """Set API keys in os.environ for chatlas to find automatically."""
        # Iterate through all fields and set environment variables using aliases
        for field_name, field_info in self.__class__.model_fields.items():
            field_value = getattr(self, field_name)
            if field_value is not None and field_info.alias:
                os.environ[field_info.alias] = field_value.get_secret_value()
        return self
