import os 
from pathlib import Path

if not os.getenv("GITHUB_ACTIONS"):
    src = Path("_site/README.md")
    dst = Path("../README.md")
    if src.exists():
        dst.write_bytes(src.read_bytes())
