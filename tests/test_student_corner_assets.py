import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def test_sample_conversation_is_populated():
    """The Student Corner sample conversation should render meaningful content."""
    conv_path = os.path.join(DATA_DIR, "sample_conversation.md")
    assert os.path.exists(conv_path), "data/sample_conversation.md is missing"

    with open(conv_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content.strip()) > 200
    assert "Student" in content and "AI Buddy" in content

def test_reflection_is_populated():
    """The reflection deliverable should be a substantial essay on AI limitations."""
    ref_path = os.path.join(DATA_DIR, "reflection.md")
    assert os.path.exists(ref_path), "data/reflection.md is missing"

    with open(ref_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content.split()) >= 300, "reflection should be ~350 words"
    assert "limitation" in content.lower() or "limits" in content.lower()