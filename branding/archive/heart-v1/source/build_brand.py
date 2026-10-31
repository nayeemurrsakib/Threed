"""Build the current threed® identity."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('build_threed_heart.py')), run_name='__main__')
