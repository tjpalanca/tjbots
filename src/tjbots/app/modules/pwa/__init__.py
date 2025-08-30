"""Progressive Web App (PWA) module for Shiny applications"""

import shutil
from pathlib import Path
from typing import Literal

from shiny import module, ui

module_dir = Path(__file__).parent


def pwa_setup(svg_logo: Path, png_logo: Path, www_dir: Path) -> dict[str, str]:
    """Set up PWA assets and return file paths for use in UI components.

    Args:
        svg_logo: Path to SVG logo file to copy.
        png_logo: Path to PNG logo file to copy.
        www_dir: Target directory for web assets.

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

    manifest_json_path = pwa_dir / "manifest.json"
    shutil.copy(module_dir / "manifest.json", manifest_json_path)
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
