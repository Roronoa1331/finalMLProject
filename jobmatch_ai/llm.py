import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import BaseModel


load_dotenv()

# Cache for transformers models to avoid reloading
_transformers_cache = {}


class LLMConfig(BaseModel):
    backend: str = "transformers"  # "transformers", "openai", "deepseek", "gemini", or "ollama"
    model: str = "Qwen/Qwen2.5-3B-Instruct"
    base_url: str | None = None
    api_key: str | None = None


def build_client(cfg: LLMConfig) -> OpenAI:
    if cfg.backend == "ollama":
        base_url = cfg.base_url or "http://localhost:11434/v1"
        api_key = cfg.api_key or "ollama"
    elif cfg.backend == "deepseek":
        base_url = cfg.base_url or "https://api.deepseek.com"
        api_key = cfg.api_key or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is required for DeepSeek backend")
    elif cfg.backend == "gemini":
        base_url = cfg.base_url or "https://generativelanguage.googleapis.com/v1beta/openai/"
        api_key = cfg.api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini backend")
    else:  # openai
        base_url = cfg.base_url or None
        api_key = cfg.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI backend")
    return OpenAI(base_url=base_url, api_key=api_key)


def complete(cfg: LLMConfig, messages: List[Dict[str, str]], temperature: float = 0.4) -> str:
    if cfg.backend == "transformers":
        return _complete_transformers(cfg, messages, temperature)
    
    client = build_client(cfg)
    try:
        resp = client.chat.completions.create(
            model=cfg.model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content  # type: ignore[index]
    except OpenAIError as exc:
        raise RuntimeError(f"LLM call failed: {exc}") from exc


def _complete_transformers(cfg: LLMConfig, messages: List[Dict[str, str]], temperature: float) -> str:
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
    except ImportError:
        raise RuntimeError("transformers and torch required for transformers backend. Install via: pip install transformers torch accelerate")
    
    model_name = cfg.model
    if model_name not in _transformers_cache:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype="auto",
                device_map="auto",
                low_cpu_mem_usage=True,
            )
            _transformers_cache[model_name] = (model, tokenizer)
        except Exception as exc:
            raise RuntimeError(f"Failed to load transformers model {model_name}: {exc}") from exc
    
    model, tokenizer = _transformers_cache[model_name]
    
    # Convert messages to prompt
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            prompt += f"System: {content}\n\n"
        elif role == "user":
            prompt += f"User: {content}\n\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n\n"
    prompt += "Assistant:"
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return response.strip()
    except Exception as exc:
        raise RuntimeError(f"Transformers inference failed: {exc}") from exc
