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


def pwa_head_content():
    """Create Progressive Web App head content configuration.
    
    Returns:
        ui.head_content: Head content with PWA meta tags and links
    """
    return ui.head_content(
        ui.tags.link(rel="stylesheet", href="custom.css"),
        ui.tags.link(rel="manifest", href="manifest.json"),
        ui.tags.link(
            rel="icon",
            type="image/svg+xml",
            size="any",
            href="assets/logo/tjbots.svg",
        ),
        ui.tags.link(
            rel="shortcut icon",
            type="image/svg+xml",
            size="any",
            href="assets/logo/tjbots.svg",
        ),
        ui.tags.link(rel="apple-touch-icon", href="assets/logo/tjbots.png"),
        ui.tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover",
        ),
        ui.tags.meta(name="mobile-web-app-capable", content="yes"),
        ui.tags.meta(
            name="apple-mobile-web-app-status-bar-style", content="default"
        ),
    )


def sidebar():
    """Create the sidebar component with dark mode toggle.
    
    Returns:
        ui.sidebar: Sidebar component with dark mode input
    """
    return ui.sidebar(ui.input_dark_mode(), open="closed")