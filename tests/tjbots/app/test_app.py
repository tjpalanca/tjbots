"""
Smoke tests for the TJBots Shiny app.

These tests verify basic functionality like app instantiation and configuration loading.
"""

import os
from unittest.mock import patch

from shiny import App

from tjbots.config import PackageConfig

# Mock environment with all AI API keys for testing
MOCK_APP_ENV = {
    "ANTHROPIC_API_KEY": "test-anthropic-key-123",
    "OPENAI_API_KEY": "test-openai-key-456",
    "GOOGLE_API_KEY": "test-google-key-789",
}


class TestAppBasics:
    """Test basic app functionality."""

    def test_config_instantiation(self):
        """Test that PackageConfig can be instantiated."""
        config = PackageConfig()
        assert config is not None
        assert hasattr(config, "anthropic_api_key")
        assert hasattr(config, "openai_api_key")
        assert hasattr(config, "google_api_key")

    @patch.dict(os.environ, MOCK_APP_ENV)
    def test_config_loads_env_vars(self):
        """Test that configuration loads environment variables."""
        config = PackageConfig()
        assert config.anthropic_api_key is not None
        assert config.anthropic_api_key.get_secret_value() == "test-anthropic-key-123"
        assert config.openai_api_key is not None
        assert config.openai_api_key.get_secret_value() == "test-openai-key-456"
        assert config.google_api_key is not None
        assert config.google_api_key.get_secret_value() == "test-google-key-789"

    @patch.dict(os.environ, MOCK_APP_ENV)
    def test_app_instantiation(self):
        """Test that the Shiny app can be instantiated without errors."""
        # Import here to avoid issues with module-level config instantiation
        from tjbots.app.app import app

        assert app is not None
        assert isinstance(app, App)
        assert app.ui is not None
        assert app.server is not None

    @patch.dict(
        os.environ,
        {
            "TJBOTS_ENV_FILE": "/tmp/nonexistent_test_file.env",
            "ANTHROPIC_API_KEY": "",
            "OPENAI_API_KEY": "",
            "GOOGLE_API_KEY": "",
        },
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
