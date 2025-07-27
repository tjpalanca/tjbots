import os 
from pathlib import Path

if not os.getenv("GITHUB_ACTIONS"):
    readme = Path("_site/README.md")
    if readme.exists():
        readme.rename("../README.md")
