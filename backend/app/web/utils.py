from pathlib import Path

from fastapi.templating import Jinja2Templates

ROOT_DIR = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(ROOT_DIR / "frontend" / "templates"))
