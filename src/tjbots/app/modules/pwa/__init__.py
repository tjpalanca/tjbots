import shutil
from pathlib import Path
from typing import Literal

from shiny import module, ui


def pwa_setup(svg_logo: Path, png_logo: Path, www_dir: Path) -> dict[str, str]:
    module_dir = Path(__file__).parent

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
