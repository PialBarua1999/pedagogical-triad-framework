"""Simple VS Code entry point. Python 3.15-compatible stdlib only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent / "src"))
from triad.__main__ import main
if __name__ == "__main__": main()
