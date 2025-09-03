"""
Smoke tests for the TJBots Shiny app.

These tests verify basic functionality like app instantiation.
"""

import logging

import pytest
import requests
from playwright.sync_api import Page
from shiny import App
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

logger = logging.getLogger(__name__)


app = create_app_fixture("../../../src/tjbots/app/app.py")


def is_responsive(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except Exception:
        return False


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

    def test_app_instantiation(self):
        """Test that the Shiny app can be instantiated without errors."""
        from tjbots.app.app import app

        assert app is not None
        assert isinstance(app, App)
        assert app.ui is not None
        assert app.server is not None

    def test_app_startup(self, page: Page, app: ShinyAppProc) -> None:
        """End-to-end smoke test to verify the app can start up and serve pages."""
        self._assert_app_loads_successfully(page, app.url, "Internal Server Error")

    @pytest.fixture(scope="session")
    def tjbots_docker_service(self, docker_ip, docker_services) -> str:
        """Return the URL for the tjbots Docker service."""
        logger.info("Starting tjbots testing service...")
        port = docker_services.port_for("app", 8080)
        url = f"http://{docker_ip}:{port}"
        docker_services.wait_until_responsive(
            timeout=60.0, pause=2, check=lambda: is_responsive(url)
        )
        return url

    def test_docker_startup(self, page: Page, tjbots_docker_service: str):
        """End-to-end smoke test to verify the Docker app can start up and serve pages."""
        self._assert_app_loads_successfully(
            page, tjbots_docker_service, "The application failed to start"
        )
