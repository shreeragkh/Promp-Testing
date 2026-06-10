import json
from src.llm import client
from src.config import MODEL

def judge_outputs(task: str, outputs: dict[str, str]) -> dict[str, dict]:
    formatted = "\n\n".join(
        f"[{label}]\n{text}" for label, text in outputs.items()
    )
    judge_prompt = f"""You are an expert evaluator. Score each response below on two criteria.

Task given to the model:
{task}

Responses to evaluate:
{formatted}

Return ONLY a JSON object. No explanation, no markdown fences. Example format:
{{
  "Zero-shot":        {{"accuracy": 7, "clarity": 8, "reasoning": "short note"}},
  "Few-shot":         {{"accuracy": 8, "clarity": 9, "reasoning": "short note"}},
  "Chain-of-Thought": {{"accuracy": 9, "clarity": 7, "reasoning": "short note"}}
}}

Scoring:
- accuracy (1-10): Is the response factually correct and complete?
- clarity (1-10): Is it easy to understand and well-structured?
"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    raw = resp.content[0].text.strip()
    # strip markdown fences if model ignores instructions
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
