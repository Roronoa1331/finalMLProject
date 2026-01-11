from __future__ import annotations

import io
import re
from typing import List, Tuple

import PyPDF2


TECH_KEYWORDS = [
    "python",
    "java",
    "c++",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "azure",
    "pytorch",
    "tensorflow",
    "pandas",
    "spark",
    "sql",
    "postgres",
    "mysql",
    "redis",
    "rabbitmq",
    "kafka",
    "react",
    "node",
    "django",
    "flask",
]


def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts).strip()
    return file_bytes.decode("utf-8", errors="ignore")


def summarize_stack(text: str) -> str:
    lower = text.lower()
    hits = [kw for kw in TECH_KEYWORDS if kw in lower]
    if not hits:
        return "No obvious tech stack detected; ask candidate to clarify strengths."
    unique_hits = sorted(set(hits))
    return "Detected stack: " + ", ".join(unique_hits)


def extract_projects(text: str, max_items: int = 5) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    projects: List[str] = []
    for ln in lines:
        if re.search(r"project|built|developed|designed", ln, re.IGNORECASE):
            projects.append(ln)
        if len(projects) >= max_items:
            break
    return projects


def analyze_resume(file_bytes: bytes, filename: str) -> Tuple[str, str, List[str]]:
    text = extract_text(file_bytes, filename)
    stack_summary = summarize_stack(text)
    projects = extract_projects(text)
    return text, stack_summary, projects
