"""
Tests for TJBots UI components.

These tests verify that UI components can be created and have the expected properties.
"""

import pytest
from htmltools import HTMLDependency, Tag
from shiny.ui._sidebar import Sidebar

from tjbots.app.ui import create_pwa_head_content, create_sidebar, create_tjbots_icon


class TestUIComponents:
    """Test UI component creation functions."""

    def test_create_tjbots_icon(self):
        """Test that the TJBots icon component can be created."""
        icon = create_tjbots_icon()
        
        # Verify it's an HTML Tag
        assert isinstance(icon, Tag)
        
        # Verify it's an img tag
        assert icon.name == "img"
        
        # Verify it has the expected attributes
        assert "style" in icon.attrs
        assert icon.attrs["style"] == "background-color: white;"
        assert "src" in icon.attrs
        assert icon.attrs["src"] == "assets/logo/tjbots.svg"

    def test_create_pwa_head_content(self):
        """Test that PWA head content can be created."""
        pwa_head = create_pwa_head_content()
        
        # Verify it's an HTMLDependency
        assert isinstance(pwa_head, HTMLDependency)
        
        # The head_content should contain multiple elements
        # We can't easily inspect the internal structure, but we can verify
        # that it was created successfully
        assert pwa_head is not None

    def test_create_sidebar(self):
        """Test that the sidebar component can be created."""
        sidebar = create_sidebar()
        
        # Verify it's a Sidebar object
        assert isinstance(sidebar, Sidebar)
        
        # Verify it was created successfully
        assert sidebar is not None

    def test_ui_components_integration(self):
        """Test that UI components can be used together like in the main app."""
        # This mimics the usage in app_ui function
        icon = create_tjbots_icon()
        sidebar = create_sidebar()
        pwa_head = create_pwa_head_content()
        
        # All components should be created successfully
        assert icon is not None
        assert sidebar is not None
        assert pwa_head is not None
        
        # Verify types
        assert isinstance(icon, Tag)
        assert isinstance(sidebar, Sidebar)
        assert isinstance(pwa_head, HTMLDependency)