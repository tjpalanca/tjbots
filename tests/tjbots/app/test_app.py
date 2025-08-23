"""
Smoke tests for the TJBots Shiny app.

These tests verify basic functionality like app instantiation.
"""

import os
from unittest.mock import patch

from playwright.sync_api import Page
from shiny import App
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

from ..test_utils import MOCK_ENV

app = create_app_fixture("/workspaces/tjbots/src/tjbots/app/app.py")


class TestAppBasics:
    """Test basic app functionality."""

    @patch.dict(os.environ, MOCK_ENV)
    def test_app_instantiation(self):
        """Test that the Shiny app can be instantiated without errors."""
        from tjbots.app.app import app

        assert app is not None
        assert isinstance(app, App)
        assert app.ui is not None
        assert app.server is not None

    def test_app_startup(self, page: Page, app: ShinyAppProc) -> None:
        """End-to-end smoke test to verify the app can start up and serve pages."""
        # Navigate to the app URL when it's ready
        page.goto(app.url)

        # Verify the page loads successfully by checking for basic elements
        # This is a minimal smoke test - just ensure we get a valid response
        page.wait_for_load_state("networkidle")

        # Check that the page title or some basic content is present
        # This verifies the app started and is serving content
        assert page.title() is not None
