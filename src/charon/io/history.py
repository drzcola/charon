from pathlib import Path
from prompt_toolkit.history import FileHistory


HISTORY_PATH = Path.home() / ".local" / "share" / "charon" / "charon_history"
HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

history = FileHistory(str(HISTORY_PATH))
