"""
Smoke tests for the TJBots configuration.

These tests verify basic functionality of the PackageConfig class.
"""

import os
from unittest.mock import patch

from tjbots.config import PackageConfig


class TestConfigBasics:
    """Test basic config functionality."""

    def test_config_loads_env_vars(self):
        """Test that configuration loads environment variables."""
        config = PackageConfig()
        assert config.anthropic_api_key is not None
        assert config.anthropic_api_key.get_secret_value() == "test-anthropic-key-123"
        assert config.openai_api_key is not None
        assert config.openai_api_key.get_secret_value() == "test-openai-key-456"
        assert config.google_api_key is not None
        assert config.google_api_key.get_secret_value() == "test-google-key-789"

    @patch.dict(
        os.environ,
        {"TJBOTS_ENV_FILE": "/tmp/nonexistent_test_file.env"},
        clear=True,
    )
    def test_config_without_api_key(self):
        """Test that config can be created even without API key (should be None or empty strings)."""
        config = PackageConfig()
        # When no API keys are provided, they should be None or empty strings
        assert (
            config.anthropic_api_key is None
            or config.anthropic_api_key.get_secret_value() == ""
        )
        assert (
            config.openai_api_key is None
            or config.openai_api_key.get_secret_value() == ""
        )
        assert (
            config.google_api_key is None
            or config.google_api_key.get_secret_value() == ""
        )
