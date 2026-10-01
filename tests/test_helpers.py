from src.utils.helpers import build_quiz_widget_key


def test_widget_key_is_stable_for_same_quiz_and_question():
    """The same quiz instance and question must map to the same key across reruns."""
    assert build_quiz_widget_key("abc123", 0) == build_quiz_widget_key("abc123", 0)


def test_widget_key_is_unique_per_question():
    """Questions within one quiz must not share a key."""
    keys = {build_quiz_widget_key("abc123", i) for i in range(5)}
    assert len(keys) == 5


def test_widget_key_differs_across_quiz_instances():
    """
    A newly loaded quiz must produce different keys for the same question index.

    Streamlit restores a widget's stored value whenever the widget key is
    unchanged, so reusing a key across quizzes would silently resubmit the
    previous quiz's answers.
    """
    previous_quiz_keys = [build_quiz_widget_key("quiz-one", i) for i in range(5)]
    new_quiz_keys = [build_quiz_widget_key("quiz-two", i) for i in range(5)]

    assert not set(previous_quiz_keys) & set(new_quiz_keys)


def test_widget_key_does_not_depend_only_on_question_index():
    """Guard against regressing to an index-only key such as 'q_0'."""
    key = build_quiz_widget_key("quiz-one", 0)

    assert "quiz-one" in key
    assert key != "q_0"
