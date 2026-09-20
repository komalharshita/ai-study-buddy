import json
import os
import pytest
from src.utils.helpers import validate_quiz_schema

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def test_sample_quiz_exists_and_is_valid():
    """The pre-set SQL Joins quiz must exist and conform to the quiz schema."""
    quiz_path = os.path.join(DATA_DIR, "sample_quiz.json")
    assert os.path.exists(quiz_path), "data/sample_quiz.json is missing"

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    assert isinstance(quiz_data, list)
    assert validate_quiz_schema(quiz_data), "sample_quiz.json does not match the required quiz schema"

def test_sample_quiz_correct_answers_are_uppercase():
    """Correct answer labels in the sample quiz must be normalized to uppercase."""
    quiz_path = os.path.join(DATA_DIR, "sample_quiz.json")
    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    for item in quiz_data:
        assert item["correct_answer"] in {"A", "B", "C", "D"}