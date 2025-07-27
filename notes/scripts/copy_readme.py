import os 
from pathlib import Path

if not os.getenv("GITHUB_ACTIONS"):
    Path("_site/README.md").rename("../README.md")
