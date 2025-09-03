"""
Tests for the sidebar component module.
"""

from playwright.sync_api import Page
from shiny.playwright import controller
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

app = create_app_fixture("sidebar_app.py")


def test_sidebar_defaults(page: Page, app: ShinyAppProc) -> None:
    """Test that both selectors load with expected defaults."""
    page.goto(app.url)

    # Controller objects for interacting with sidebar components
    provider_select = controller.InputSelect(page, "sidebar-selected_provider")
    model_select = controller.InputSelect(page, "sidebar-selected_model")

    # Check default provider (should be first in MODEL_PROVIDER_CHOICES)
    provider_select.expect_selected("anthropic")

    # Check default model for anthropic provider
    model_select.expect_selected("claude-sonnet-4-20250514")


def test_provider_change_updates_model_selector(page: Page, app: ShinyAppProc) -> None:
    """Test that changing provider updates model selector."""
    page.goto(app.url)

    provider_select = controller.InputSelect(page, "sidebar-selected_provider")
    model_select = controller.InputSelect(page, "sidebar-selected_model")

    # Change provider to Google
    provider_select.set("google")

    # Verify model selector updates to Google's default
    model_select.expect_selected("gemini-2.5-flash")


def test_sidebar_return_values(page: Page, app: ShinyAppProc) -> None:
    """Test that the module returns expected input values."""
    page.goto(app.url)

    provider_select = controller.InputSelect(page, "sidebar-selected_provider")
    model_select = controller.InputSelect(page, "sidebar-selected_model")
    provider_output = controller.OutputText(page, "selected_provider_text")
    model_output = controller.OutputText(page, "selected_model_text")

    # Test initial return values
    provider_output.expect_value("Provider: anthropic")
    model_output.expect_value("Model: claude-sonnet-4-20250514")

    # Change selections and test updated return values
    provider_select.set("openai")
    model_select.set("gpt-4.1")

    provider_output.expect_value("Provider: openai")
    model_output.expect_value("Model: gpt-4.1")
