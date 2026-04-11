"""
Replicate API Wrapper
=====================
Handles API calls with retry logic, rate limiting, disk caching, and JSONL logging.
"""

import os
import time
import json
import hashlib
from datetime import datetime

import replicate
import sys
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import (
    REPLICATE_API_TOKEN,
    OPENROUTER_API_KEY,
    MODELS,
    MAX_TOKENS,
    TOP_P,
    CACHE_DIR,
    RAW_DIR,
    MAX_REQUESTS_PER_MINUTE,
)


class ReplicateModel:
    """Wrapper around the Replicate API with caching, rate-limiting, and logging."""

    def __init__(self):
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        self.client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        self.cache_dir = CACHE_DIR
        self.log_path = os.path.join(RAW_DIR, "api_log.jsonl")
        os.makedirs(self.cache_dir, exist_ok=True)

        # Simple rate-limiter state
        self._call_timestamps: list[float] = []
        self._max_rpm = MAX_REQUESTS_PER_MINUTE

        # Aggregate stats
        self.total_calls = 0
        self.cached_calls = 0
        self.total_latency = 0.0

    # ── Cache helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _cache_key(model_id: str, prompt: str, system_prompt: str, temperature: float) -> str:
        raw = json.dumps(
            {"model_id": model_id, "prompt": prompt,
             "system_prompt": system_prompt, "temperature": temperature},
            sort_keys=True,
        )
        return hashlib.sha256(raw.encode()).hexdigest()

    def _cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def _read_cache(self, key: str) -> dict | None:
        path = self._cache_path(key)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _write_cache(self, key: str, data: dict) -> None:
        with open(self._cache_path(key), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    # ── Rate limiter ─────────────────────────────────────────────────────────

    def _wait_for_rate_limit(self) -> None:
        now = time.time()
        # Purge timestamps older than 60 s
        self._call_timestamps = [t for t in self._call_timestamps if now - t < 60]
        if len(self._call_timestamps) >= self._max_rpm:
            sleep_time = 60 - (now - self._call_timestamps[0]) + 0.1
            if sleep_time > 0:
                time.sleep(sleep_time)
        self._call_timestamps.append(time.time())

    # ── Logging ──────────────────────────────────────────────────────────────

    def _log_call(self, record: dict) -> None:
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    # ── Input schema detection & Routing ─────────────────────────────────────

    # Providers routed to OpenRouter API (OpenAI-compatible)
    _OPENROUTER_PROVIDERS = {
        "openai", "anthropic", "google", "xai",
        "deepseek-ai", "qwen", "moonshotai", "ibm-granite",
    }

    # Providers routed to Replicate API
    _REPLICATE_PROVIDERS = {
        "meta", "mistralai", "google-deepmind", "stability-ai",
        "replicate", "yorickvp",
    }

    # ── Core generate ────────────────────────────────────────────────────────

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=120),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    def _call_api(self, model_id: str, prompt: str, system_prompt: str,
                  temperature: float) -> str:
        """Run the prediction and return concatenated text output.

        Routes strictly to Replicate, which universally requires the 'prompt' parameter
        for all proxies (OpenAI, Google, Anthropic, DeepSeek, open-source).
        """
        temp = max(temperature, 0.1)  # Increased minimum to 0.1 to prevent underflow silence

        input_payload = {
            "max_tokens": MAX_TOKENS,
            "top_p": TOP_P,
            "temperature": temp,
        }
        
        os_providers = {"meta", "mistralai", "google-deepmind", "stability-ai", "replicate"}
        provider = model_id.split("/")[0]
        
        if "kimi-k2.5" in model_id:
            input_payload.update({
                "temperature": 0.1,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            })
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
                
        elif "qwen" in model_id:
            input_payload.update({
                "temperature": 0.1,
                "top_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            })
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
                
        elif "granite" in model_id:
            input_payload.update({
                "top_k": 50,
                "top_p": 0.9,
                "max_tokens": 512,
                "min_tokens": 0,
                "temperature": 0.6,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "stop": [],
                "tools": [],
                "messages": [],
                "documents": [],
                "chat_template_kwargs": {},
                "add_generation_prompt": True
            })
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
                
        elif "meta-llama-3" in model_id:
            input_payload.update({
                "temperature": 0.6,
                "top_k": 0,
                "top_p": 0.9,
                "max_tokens": 512,
                "min_tokens": 0,
                "length_penalty": 1,
                "presence_penalty": 1.15,
                "log_performance_metrics": False
            })
            if "instruct" in model_id:
                sys_part = "<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>" if system_prompt else ""
                input_payload.update({
                    "stop_sequences": "<|end_of_text|>,<|eot_id|>",
                    "prompt_template": f"<|begin_of_text|>{sys_part}<|start_header_id|>user<|end_header_id|>\n\n{{prompt}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
                })
                input_payload["prompt"] = prompt
                if system_prompt:
                    input_payload["system_prompt"] = system_prompt
            else:
                input_payload.update({
                    "prompt_template": "{prompt}"
                })
                # Force fill-in-the-blanks completion for base models
                input_payload["prompt"] = f"{prompt}\n\nMy responses are:\nDONATION: $"

        elif "gemma" in model_id:
            input_payload.update({
                "top_k": 50,
                "top_p": 0.95,
                "min_new_tokens": -1,
                "repetition_penalty": 1.15,
                "max_new_tokens": input_payload.pop("max_tokens", 1024)
            })
            if system_prompt:
                input_payload["prompt"] = f"{system_prompt}\n\n{prompt}"
            else:
                input_payload["prompt"] = prompt

        elif "gemini-2.5-flash" in model_id:
            input_payload.update({
                "top_p": 0.95,
                "dynamic_thinking": False,
                "max_output_tokens": MAX_TOKENS,
                "images": [],
                "videos": [],
            })
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
        elif "gpt-oss" in model_id:
            input_payload.update({
                "presence_penalty": 0,
                "frequency_penalty": 0,
            })
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
        elif provider in os_providers:
            input_payload["prompt"] = prompt
            if system_prompt:
                input_payload["system_prompt"] = system_prompt
        else:
            if system_prompt:
                input_payload["prompt"] = f"System Instruction: {system_prompt}\n\nUser: {prompt}"
            else:
                input_payload["prompt"] = prompt
        if "kimi" in model_id:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": "moonshotai/kimi-k2.5",
                "messages": messages,
                "temperature": 0.1,
                "top_p": 1,
                "reasoning": {"enabled": True}
            }
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            resp_json = response.json()
            output = resp_json['choices'][0]['message'].get('content', '')
        else:
            output = self.client.run(model_id, input=input_payload)

        # Replicate can return different formats
        response_text = ""
        if isinstance(output, str):
            response_text = output
        elif isinstance(output, dict):
            if "output" in output:
                response_text = output["output"]
            elif "choices" in output and output["choices"]:
                response_text = output["choices"][0].get("message", {}).get("content", str(output))
            else:
                response_text = str(output)
        else:
            response_text = "".join(str(chunk) for chunk in output)
            
        if "meta-llama-3" in model_id and "instruct" not in model_id:
            response_text = "DONATION: $" + response_text

        if not response_text.strip():
            raise ValueError(f"API generated an empty response for {model_id}.")
            
        return response_text

    def generate(
        self,
        model_key: str,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
    ) -> dict:
        """
        Generate a response, using cache if available.

        Returns
        -------
        dict with keys: response_text, model_key, model_id, temperature,
        prompt, system_prompt, timestamp, cached, latency_seconds
        """
        model_id = MODELS[model_key]
        cache_key = self._cache_key(model_id, prompt, system_prompt, temperature)

        # Check cache
        cached = self._read_cache(cache_key)
        if cached is not None:
            self.cached_calls += 1
            self.total_calls += 1
            cached["cached"] = True
            return cached

        # Rate limit & call API
        self._wait_for_rate_limit()

        t0 = time.time()
        try:
            response_text = self._call_api(model_id, prompt, system_prompt, temperature)
            latency = time.time() - t0
        except Exception as e:
            latency = time.time() - t0
            result = {
                "response_text": f"API_ERROR: {e}",
                "model_key": model_key,
                "model_id": model_id,
                "temperature": temperature,
                "prompt": prompt,
                "system_prompt": system_prompt,
                "timestamp": datetime.utcnow().isoformat(),
                "cached": False,
                "latency_seconds": latency,
            }
            self._log_call({**result, "status": "error", "error": str(e)})
            self.total_calls += 1
            return result

        result = {
            "response_text": response_text,
            "model_key": model_key,
            "model_id": model_id,
            "temperature": temperature,
            "prompt": prompt,
            "system_prompt": system_prompt,
            "timestamp": datetime.utcnow().isoformat(),
            "cached": False,
            "latency_seconds": latency,
        }

        # Cache and log
        self._write_cache(cache_key, result)
        self._log_call({**result, "status": "success"})
        self.total_calls += 1
        self.total_latency += latency

        return result

    def stats(self) -> dict:
        return {
            "total_calls": self.total_calls,
            "cached_calls": self.cached_calls,
            "api_calls": self.total_calls - self.cached_calls,
            "total_latency_seconds": round(self.total_latency, 2),
        }
