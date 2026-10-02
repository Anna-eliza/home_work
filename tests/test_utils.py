import json
import os
import tempfile

from src.utils import load_operations


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, "data", "operations.json")


def test_load_existing_file():
    result = load_operations(PATH)
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
        f.write("{invalid json")   # ← латиница!
        path = f.name
    try:
        assert load_operations(path) == []
    finally:
        os.remove(path)