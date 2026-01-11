# Technical Report Outline

1. Prompt Engineering
   - System prompt persona and structure (introduction, technical, behavioral, conclusion).
   - Few-shot style: resume-grounded first questions; memory retention via chat history.
   - Safety and concision constraints (<=120 words guidance).

2. Architecture
   - Streamlit UI: resume upload, interview loop, evaluation, sandbox.
   - LLM backend abstraction: OpenAI or Ollama via `LLMConfig`.
   - Resume parsing: PDF/text extraction, tech stack heuristics, project detection.
   - Interview flow manager: stage counters for intro, technical, behavioral, conclusion.
   - Coding sandbox: constrained Python exec with safe built-ins.

3. Advanced Track (B: Coding Sandbox)
   - Sandbox design and limitations; advise offline/full isolation for production.
   - Optional diagram: UI -> LLM -> Sandbox feedback loop.

4. Evaluation
   - Markdown report template: score, strengths, weaknesses, sample answers.
   - Scoring heuristics left to LLM with structured instructions.

5. Future Work
   - Vector store for reusable question bank (Chroma/FAISS).
   - Audio input, richer analytics, automated difficulty adjustment.
