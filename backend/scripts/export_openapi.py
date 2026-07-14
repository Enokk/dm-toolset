import json
from pathlib import Path

from dm_toolset_backend.main import app

output_path = Path(__file__).resolve().parent.parent / "openapi.json"
output_path.write_text(json.dumps(app.openapi(), indent=2))
