# API & Integration Documentation: AI Learning Buddy

This document details how the **AI Learning Buddy** integrates with the Google Gemini API, including model details, generation parameters, and prompt schemas.

---

## 1. Google Gemini SDK Integration
The project uses the official Google GenAI Python SDK (`google-genai`).

### Configuration
The client configuration is initialized in `src/core/gemini_client.py`:
```python
from google import genai
client = genai.Client(api_key=api_key)
```

---

## 2. API Generation Parameters
We apply specific configurations to control response creativity and output limits:

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Model** | `gemini-1.5-flash` / `gemini-2.0-flash` | Lightweight, fast, optimized for conversational workflows and JSON output. |
| **Temperature** | `0.7` | Balances creativity and instruction-following. High enough for rich analogies; low enough to prevent quiz structure breaking. |
| **Top P** | `0.95` | Controls vocabulary selection diversity. |
| **Max Output Tokens** | `2048` | Caps response sizes to prevent run-on answers and manage token utilization. |

---

## 3. Core Prompts & Schemas

### Concept Explanation Prompt
* **Method:** `PromptTemplates.get_explain_concept_prompt(topic)`
* **Objective:** Explain the topic simply using structural headings.
* **Prompt Structure:**
  ```text
  Explain the concept of '[topic]' in simple language for a beginner.
  Requirements:
  - Define the concept clearly in 1-2 sentences.
  - Break down the explanation into 3-4 key sub-points with bold headings.
  - Use simple terminology and a friendly, encouraging tone.
  - Conclude with a short summary or takeaway.
  ```

### Real-Life Example Prompt
* **Method:** `PromptTemplates.get_real_life_example_prompt(topic)`
* **Objective:** Create a relatable analogy.
* **Prompt Structure:**
  ```text
  Provide one simple, highly relatable real-life example or analogy of '[topic]' that a layperson can easily understand.
  Requirements:
  - Start with a clear scenario (e.g., 'Imagine you are...').
  - Explain how the concept applies directly to this scenario.
  - Highlight why this example represents '[topic]'.
  ```

### Quiz Generation (Structured Output)
* **Method:** `PromptTemplates.get_generate_quiz_prompt(topic)`
* **Objective:** Enforce JSON formatting to facilitate interactive parsing.
* **Prompt Structure:**
  ```text
  Create a 5-question multiple-choice quiz about '[topic]'.
  Requirements:
  ...
  You MUST format the output strictly as a JSON list of objects, and return ONLY this JSON.
  ...
  JSON schema:
  [
    {
      "id": 1,
      "question": "...",
      "options": {
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      },
      "correct_answer": "A/B/C/D",
      "explanation": "..."
    }
  ]
  ```

### Feedback & Answer Evaluation Prompt
* **Method:** `PromptTemplates.get_feedback_prompt(question, options, correct_answer, user_answer, explanation)`
* **Objective:** Praise correct responses or gently correct incorrect options.
* **Prompt Structure:**
  ```text
  Evaluate the learner's response to the following multiple-choice question.
  ...
  Please evaluate their answer and write a response.
  Requirements:
  - If the learner is correct, start with enthusiastic praise.
  - If the learner is incorrect, be supportive and encouraging.
  - Provide a clear, simple explanation.
  ```
