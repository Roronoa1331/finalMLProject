from typing import List, Dict

from .llm import LLMConfig, complete
from .prompts import evaluation_prompt


def generate_evaluation(cfg: LLMConfig, transcript: List[Dict[str, str]]) -> str:
    prompt = evaluation_prompt(transcript)
    messages = [
        {"role": "system", "content": "You create concise, actionable interview evaluations."},
        {"role": "user", "content": prompt},
    ]
    return complete(cfg, messages, temperature=0.2)
