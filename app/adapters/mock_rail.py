import json
from pathlib import Path

from app.adapters.base import RailAdapter


class MockRailAdapter(RailAdapter):
    source_name = "mock_rail"

    def fetch(self) -> list[dict]:
        path = Path("sample_data/railway_features.json")
        return json.loads(path.read_text())
