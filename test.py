import os, pathlib
import pytest

os.chdir( pathlib.Path.cwd() / 'code/test' )

pytest.main()