"""
Bots Shiny Application

Test harness for configuring and testing various bot and tool combinations.
"""

from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory

import chatlas
from shiny import App, Inputs, Outputs, Session, ui

from tjbots.app.components.chat import chat_server, chat_ui
from tjbots.app.components.sidebar import sidebar_server, sidebar_ui
from tjbots.app.modules.pwa import pwa_ui
from tjbots.app.modules.reconnect import reconnect_ui
from tjbots.config import PackageConfig

config = PackageConfig()

app_dir = Path(__file__).parent
www_tempdir = TemporaryDirectory("tjbots_app_www")
www_dir = Path(www_tempdir.name)
assets_dir = app_dir.parent.parent.parent / "assets"


app_ui = ui.page_sidebar(
    sidebar_ui("sidebar"),
    pwa_ui(
        "pwa",
        png_logo=assets_dir / "logo" / "tjbots.png",
        svg_logo=assets_dir / "logo" / "tjbots.svg",
        www_dir=www_dir,
        app_name="TJBots",
        start_url="https://bots.tjpalanca.com",
        background_color="#000000",
        theme_color="#008080",
        description="TJ's adventures with LLMs",
    ),
    reconnect_ui("reconnect"),
    chat_ui("chat"),
    window_title="TJBots",
    fillable=True,
    fillable_mobile=True,
)


@dataclass
class Context:
    turns: list[chatlas.Turn] = field(default_factory=list)


def app_server(input: Inputs, output: Outputs, session: Session):
    PackageConfig()
    context = Context()
    selected_provider, selected_model = sidebar_server("sidebar")
    chat_server(
        "chat",
        selected_provider=selected_provider,
        selected_model=selected_model,
        context=context,
    )


app = App(
    app_ui,
    app_server,
    static_assets={"/": www_dir},
)
app.on_shutdown(lambda: www_tempdir.cleanup())
