"""Launcher: run `python main.py` from the repository root."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from pacman.main import main  # noqa: E402

if __name__ == "__main__":
    main()
