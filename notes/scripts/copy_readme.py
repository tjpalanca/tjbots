import os 
from pathlib import Path

if not os.getenv("GITHUB_ACTIONS"):
    readme = Path("_site/README.md")
    if readme.is_file():
        readme.rename("../README.md")
