import json
import os
import tempfile

from utils import load_operations


def test_load_existing_file():
    # путь к реальному файлу
    path = os.path.join("data", "operations.json")
    result = load_operations(path)
    assert isinstance(result, list)
    assert len(result) > 0


def test_file_not_found():
    assert load_operations("data/nope.json") == []


def test_empty_file():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        assert load_operations(path) == []
    finally:
        os.remove(path)


def test_not_a_list():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"a": 1}, f)
        path = f.name
    try:
        assert load_operations(path) == []
    finally:
        os.remove(path)


def test_broken_json():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write("{невалидный json")
        path = f.name
    try:
        assert load_operations(path) == []
    finally:
        os.remove(path)