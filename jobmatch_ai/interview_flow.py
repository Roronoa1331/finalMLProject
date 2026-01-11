from __future__ import annotations

from typing import List, Dict

INTRO_TARGET = 1
TECH_MIN, TECH_MAX = 3, 5
BEHAVIORAL_MIN = 1


class InterviewState:
    def __init__(self) -> None:
        self.stage = "intro"
        self.tech_count = 0
        self.behavior_count = 0

    def next_directive(self) -> str:
        if self.stage == "intro" and self.tech_count == 0:
            self.stage = "technical"
            return "Begin with a concise introduction and ask the candidate for a self-intro."

        if self.stage == "technical":
            self.tech_count += 1
            if self.tech_count < TECH_MAX:
                return "Ask a technical question. Prefer resume-grounded for the first 2-3."
            self.stage = "behavioral"

        if self.stage == "behavioral":
            self.behavior_count += 1
            if self.behavior_count < BEHAVIORAL_MIN:
                return "Ask a behavioral question (failure, conflict, ownership)."
            self.stage = "conclusion"

        return "Politely conclude the interview."


def build_chat(system_prompt: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{"role": "system", "content": system_prompt}, *history]
