import shutil
import sys
from pathlib import Path

python_exe = Path(sys.executable)  # .with_stem("python")
print("Copying python executable:", python_exe)
shutil.copy(python_exe, "dist/vuegen_gui/python")
print("Done.")
