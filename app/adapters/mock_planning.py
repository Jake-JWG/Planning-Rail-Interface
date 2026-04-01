import json
from pathlib import Path

from app.adapters.base import PlanningAdapter


class MockPlanningAdapter(PlanningAdapter):
    source_name = "mock_planning"

    def fetch(self) -> list[dict]:
        path = Path("sample_data/planning_applications.json")
        return json.loads(path.read_text())
