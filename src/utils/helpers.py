import json
import re
from typing import List, Dict, Any, Optional
from src.logger import logger

def extract_json_from_text(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Extracts a JSON list from a text block, handling common LLM formatting behaviors
    such as wrapping JSON in markdown blocks (e.g., ```json ... ```).
    
    Args:
        text: Raw text string potentially containing JSON.
        
    Returns:
        A list of dictionaries if successful, otherwise None.
    """
    if not text:
        return None
        
    # Clean the input text first
    cleaned = text.strip()
    
    # Check for markdown code block markers
    markdown_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
    if markdown_match:
        cleaned = markdown_match.group(1).strip()
        
    # Find matching brackets to extract just the list/object
    list_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', cleaned)
    if list_match:
        cleaned = list_match.group(0)

    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Wrap single object in a list for consistency
            return [data]
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}\nRaw block analyzed: {cleaned[:200]}...")
        return None

def validate_quiz_schema(quiz_list: List[Dict[str, Any]]) -> bool:
    """
    Validates that the parsed quiz list conforms strictly to our schema.
    Schema requires:
    - Exactly 5 questions
    - Each question must contain: 'id', 'question', 'options', 'correct_answer', 'explanation'
    - 'options' must be a dictionary with keys 'A', 'B', 'C', 'D'
    - 'correct_answer' must be one of 'A', 'B', 'C', 'D'
    
    Args:
        quiz_list: A list of parsed dictionaries.
        
    Returns:
        True if the schema is correct, False otherwise.
    """
    if not quiz_list or len(quiz_list) != 5:
        logger.warning(f"Quiz validation failed: expected 5 items, got {len(quiz_list) if quiz_list else 0}")
        return False
        
    required_keys = {"id", "question", "options", "correct_answer", "explanation"}
    valid_answers = {"A", "B", "C", "D"}
    
    for idx, item in enumerate(quiz_list):
        # Check all keys are present
        if not required_keys.issubset(item.keys()):
            missing = required_keys - item.keys()
            logger.warning(f"Quiz item {idx} is missing keys: {missing}")
            return False
            
        # Validate options structure
        options = item["options"]
        if not isinstance(options, dict) or not set(options.keys()) == valid_answers:
            logger.warning(f"Quiz item {idx} options are invalid. Expected keys A, B, C, D. Got: {options}")
            return False
            
        # Validate correct answer label
        ans = str(item["correct_answer"]).strip().upper()
        if ans not in valid_answers:
            logger.warning(f"Quiz item {idx} correct_answer '{ans}' is invalid.")
            return False
            
        # Standardize correct answer to uppercase
        item["correct_answer"] = ans

    return True

def build_quiz_widget_key(quiz_instance_id: str, question_index: int) -> str:
    """
    Builds the Streamlit widget key for a single quiz answer control.

    The key must be scoped to the quiz instance. When a widget is created with
    an explicit ``key``, Streamlit treats that key as the widget's identity and
    restores the stored value on the next rerun, ignoring ``index``. Scoping by
    question index alone would therefore reattach the answer controls of a
    previously loaded quiz, and those stale selections would be graded against
    the new quiz.

    Args:
        quiz_instance_id: Identifier of the currently loaded quiz. A new value
            must be generated whenever a different quiz is loaded.
        question_index: Zero-based index of the question within the quiz.

    Returns:
        A widget key unique to this quiz instance and question.
    """
    return f"q_{quiz_instance_id}_{question_index}"
