"""
Smoke tests for the TJBots Shiny app.

These tests verify basic functionality like app instantiation.
"""

import os
from unittest.mock import patch

from shiny import App

from ..test_utils import MOCK_ENV


class TestAppBasics:
    """Test basic app functionality."""

    @patch.dict(os.environ, MOCK_ENV)
    def test_app_instantiation(self):
        """Test that the Shiny app can be instantiated without errors."""
        # Import here to avoid issues with module-level config instantiation
        from tjbots.app.app import app

        assert app is not None
        assert isinstance(app, App)
        assert app.ui is not None
        assert app.server is not None
