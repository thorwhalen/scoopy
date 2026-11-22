"""Keep scoopy's import-time app-data folder inside a temp dir."""

import os
import tempfile

os.environ.setdefault("SCOOPY_APP_DATA_DIR", tempfile.mkdtemp(prefix="scoopy_test_"))
