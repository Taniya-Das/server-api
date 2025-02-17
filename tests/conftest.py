import json
from pathlib import Path
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture()
def api_client() -> Generator[FastAPI, None, None]:
    # We want to avoid starting a test client app if tests don't need it.
    from main import app

    return TestClient(app)


@pytest.fixture()
def dataset_130() -> Generator[dict[str, Any], None, None]:
    json_path = Path(__file__).parent / "resources" / "datasets" / "dataset_130.json"
    with json_path.open("r") as dataset_file:
        yield json.load(dataset_file)


@pytest.fixture()
def default_configuration_file() -> Path:
    return Path().parent.parent / "src" / "config.toml"
