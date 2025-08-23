"""
Smoke tests for the TJBots Shiny app.

These tests verify basic functionality like app instantiation.
"""

import os
from unittest.mock import patch

import pytest
from playwright.sync_api import Page
from shiny import App
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

from ..test_utils import MOCK_ENV

app = create_app_fixture("../../../src/tjbots/app/app.py")


class TestAppBasics:
    """Test basic app functionality."""

    def _assert_app_loads_successfully(
        self, page: Page, url: str, error_text: str
    ) -> None:
        """Helper method to verify an app loads without errors."""
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page_content = page.content()

        assert error_text not in page_content

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
        self._assert_app_loads_successfully(page, app.url, "Internal Server Error")

    @pytest.fixture(scope="session")
    def tjbots_docker_service(self, docker_ip, docker_services):
        """Return the URL for the tjbots Docker service."""
        port = docker_services.port_for("tjbots", 8080)
        return f"http://{docker_ip}:{port}"

    @patch.dict(os.environ, MOCK_ENV)
    def test_docker_startup(self, page: Page, tjbots_docker_service):
        """End-to-end smoke test to verify the Docker app can start up and serve pages."""
        self._assert_app_loads_successfully(
            page, tjbots_docker_service, "The application failed to start"
        )
