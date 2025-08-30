"""Shiny module for maintaining connections"""

from pathlib import Path

from shiny import module, ui

module_dir = Path(__file__).parent


@module.ui
def reconnect_ui():
    """Add reconnection UI components

    This adds a script that indicates that reconnection is enabled for this app; only
    available when run in a Shiny server instance."""
    return ui.head_content(ui.include_js(module_dir / "reconnect.js"))
