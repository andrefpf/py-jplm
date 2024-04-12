from pathlib import Path

from .config import Config
from .runner import JPLMRunner
from .pgx import PGXReader


PY_JPLM_DIR = Path(__file__).parent
PY_JPLM_DEFAULT_BIN = PY_JPLM_DIR / "bin"