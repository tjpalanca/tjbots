import os

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PackageConfig(BaseSettings):
    """
    Configuration and control plane for the TJBots Package
    """

    openai_api_key: SecretStr | None = Field(
        alias="OPENAI_API_KEY",
        default=None,
        json_schema_extra={"set_in_environ": True},
    )
    google_api_key: SecretStr | None = Field(
        alias="GOOGLE_API_KEY",
        default=None,
        json_schema_extra={"set_in_environ": True},
    )
    anthropic_api_key: SecretStr | None = Field(
        alias="ANTHROPIC_API_KEY",
        default=None,
        json_schema_extra={"set_in_environ": True},
    )

    model_config = SettingsConfigDict(
        env_file=os.getenv("TJBOTS_ENV_FILE", "/run/secrets/tjbots.env")
    )

    @model_validator(mode="after")
    def set_environ(self):
        """Set environment variables for fields with set_in_environ == True"""

        # Iterate through all fields and set environment variables using aliases
        for field_name, field_info in self.__class__.model_fields.items():
            field_value = getattr(self, field_name)
            # Check if field should be set in environment
            set_in_environ = (
                field_info.json_schema_extra
                and field_info.json_schema_extra.get("set_in_environ", False)
            )
            # Set in environment if conditions allow
            if field_value is not None and field_info.alias and set_in_environ:
                os.environ[field_info.alias] = field_value.get_secret_value()
        return self
