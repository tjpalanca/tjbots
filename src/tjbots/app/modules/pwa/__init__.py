"""Progressive Web App (PWA) module for Shiny applications"""

import json
import shutil
from pathlib import Path
from typing import Literal

from shiny import module, ui

module_dir = Path(__file__).parent


def pwa_setup(
    svg_logo: Path,
    png_logo: Path,
    www_dir: Path,
    app_name: str,
    start_url: str,
    background_color: str,
    theme_color: str,
    description: str,
    app_short_name: str | None = None,
    display: str = "standalone",
) -> dict[str, str]:
    """Set up PWA assets and return file paths for use in UI components.

    Args:
        svg_logo: Path to SVG logo file to copy.
        png_logo: Path to PNG logo file to copy.
        www_dir: Target directory for web assets.
        app_name: Name of the application for the PWA manifest.
        start_url: The URL that loads when the PWA is launched.
        background_color: Background color for the PWA splash screen.
        theme_color: Theme color for the PWA UI elements.
        description: Description of the PWA.
        app_short_name: Short name for the PWA manifest. Defaults to app_name if not provided.
        display: Display mode for the PWA (standalone, fullscreen, minimal-ui, browser).

    Returns:
        Dictionary mapping asset types to their relative paths.
    """
    pwa_dir = www_dir / "pwa"
    pwa_dir.mkdir(parents=True, exist_ok=True)

    svg_logo_path = pwa_dir / "logo.svg"
    shutil.copy(svg_logo, svg_logo_path)
    svg_logo_href = str(svg_logo_path.relative_to(www_dir))

    png_logo_path = pwa_dir / "logo.png"
    shutil.copy(png_logo, png_logo_path)
    png_logo_href = str(png_logo_path.relative_to(www_dir))

    pwa_css_path = pwa_dir / "pwa.css"
    shutil.copy(module_dir / "pwa.css", pwa_css_path)
    pwa_css_href = str(pwa_css_path.relative_to(www_dir))

    # Generate manifest.json programmatically
    manifest_data = {
        "name": app_name,
        "short_name": app_short_name if app_short_name is not None else app_name,
        "start_url": start_url,
        "display": display,
        "background_color": background_color,
        "theme_color": theme_color,
        "description": description,
        "icons": [
            {
                "src": svg_logo_href,
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            }
        ],
    }

    manifest_json_path = pwa_dir / "manifest.json"
    with open(manifest_json_path, "w") as f:
        json.dump(manifest_data, f, indent=4)
    manifest_json_href = str(manifest_json_path.relative_to(www_dir))

    return {
        "png_logo": png_logo_href,
        "svg_logo": svg_logo_href,
        "pwa_css": pwa_css_href,
        "manifest_json": manifest_json_href,
    }


@module.ui
def pwa_ui(
    pwa_hrefs: dict[str, str],
    status_bar: Literal["default", "black-translucent", "black-opaque"] = "default",
):
    """Generate PWA-compatible HTML head content for Shiny apps.

    Args:
        pwa_hrefs: Dictionary of asset paths from pwa_setup().
        status_bar: iOS status bar style for mobile web apps.

    Returns:
        Shiny UI head content with PWA meta tags and links.
    """
    return ui.head_content(
        ui.tags.link(rel="stylesheet", href=pwa_hrefs["pwa_css"]),
        ui.tags.link(rel="manifest", href=pwa_hrefs["manifest_json"]),
        ui.tags.link(
            rel="icon",
            type="image/svg+xml",
            size="any",
            href=pwa_hrefs["svg_logo"],
        ),
        ui.tags.link(
            rel="shortcut icon",
            type="image/svg+xml",
            size="any",
            href=pwa_hrefs["svg_logo"],
        ),
        ui.tags.link(rel="apple-touch-icon", href=pwa_hrefs["png_logo"]),
        ui.tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover",
        ),
        ui.tags.meta(name="mobile-web-app-capable", content="yes"),
        ui.tags.meta(name="apple-mobile-web-app-status-bar-style", content=status_bar),
    )
