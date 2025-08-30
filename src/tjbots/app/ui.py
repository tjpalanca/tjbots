"""
UI Components for TJBots Shiny Application

This module contains reusable UI components for the TJBots application,
including Progressive Web App configuration, branding, and layout components.
"""

from shiny import ui


def tjbots_icon():
    """Create the TJBots logo component.

    Returns:
        ui.img: Image component for the TJBots logo
    """
    return ui.img(style="background-color: white;", src="assets/logo/tjbots.svg")


def sidebar():
    """Create the sidebar component with dark mode toggle.

    Returns:
        ui.sidebar: Sidebar component with dark mode input
    """
    return ui.sidebar(ui.input_dark_mode(), open="closed")
