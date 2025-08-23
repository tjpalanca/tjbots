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

app = create_app_fixture("../../../src/tjbots/app/app.py")


class TestAppBasics:
    """Test basic app functionality."""

    @patch.dict(os.environ, MOCK_ENV)
    def test_app_instantiation(self):
        """Test that the Shiny app can be instantiated without errors."""
        from tjbots.app.app import app, app_ui

        assert app is not None
        assert isinstance(app, App)
        assert app.ui is not None
        assert app.server is not None

        # Test that the UI function can be executed without exceptions
        ui_result = app_ui(None)
        assert ui_result is not None

    def test_app_startup(self, page: Page, app: ShinyAppProc) -> None:
        """End-to-end smoke test to verify the app can start up and serve pages."""
        # Navigate to the app URL when it's ready
        page.goto(app.url)

        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")

        # Check for any error messages in the page content
        page_content = page.content()

        # Verify no error indicators are present - keep it simple
        assert "Internal Server Error" not in page_content, (
            "Page shows 'Internal Server Error' - app failed to load"
        )
