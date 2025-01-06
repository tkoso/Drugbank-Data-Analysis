import sys
from pathlib import Path

# this file is loaded when pytest is run on our `tests` folder
# this way we can acess files from `src` folder without any issues
src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_path))