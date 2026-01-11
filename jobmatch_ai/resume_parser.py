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


def extract_candidate_name(text: str) -> str:
    """Extract candidate name from resume (usually first line or before email)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "Candidate"
    
    # Try to find name (usually first non-empty line that's not a title)
    for line in lines[:5]:
        # Skip common headers and emails
        if any(skip in line.lower() for skip in ["email", "phone", "linkedin", "@"]):
            continue
        # Return the first line that looks like a name (short, capitalized)
        if len(line) < 50 and line[0].isupper():
            return line.strip()
    
    return "Candidate"


def analyze_resume(file_bytes: bytes, filename: str) -> Tuple[str, str, List[str], str]:
    text = extract_text(file_bytes, filename)
    stack_summary = summarize_stack(text)
    projects = extract_projects(text)
    candidate_name = extract_candidate_name(text)
    return text, stack_summary, projects, candidate_name
