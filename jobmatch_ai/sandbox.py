import contextlib
import io
from typing import Dict

SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "range": range,
    "enumerate": enumerate,
    "sorted": sorted,
    "print": print,
}


class SandboxResult:
    def __init__(self, stdout: str, error: str | None):
        self.stdout = stdout
        self.error = error


def run_code_snippet(code: str) -> SandboxResult:
    sandbox_globals: Dict[str, object] = {"__builtins__": SAFE_BUILTINS}
    stdout_buffer = io.StringIO()
    error_text: str | None = None
    try:
        with contextlib.redirect_stdout(stdout_buffer):
            exec(code, sandbox_globals)
    except Exception as exc:  # broad catch for feedback to user; sandbox is constrained
        error_text = f"{exc.__class__.__name__}: {exc}"
    return SandboxResult(stdout=stdout_buffer.getvalue(), error=error_text)
