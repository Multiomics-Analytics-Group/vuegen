import shutil
import sys
from pathlib import Path

python_exe = Path(sys.executable).with_stem("python")
shutil.copy(python_exe, "dist/vuegen_gui/_internal")
