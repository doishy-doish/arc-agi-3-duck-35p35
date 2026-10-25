# Run the 35.35 harness against YOUR models (CPU path, additive only)

Nothing about the GPU/Kaggle path changes. These env vars + `--model local` redirect the
analyzer (ToolAgent) to any OpenAI-compatible server. SGLang is simply never booted.

## 1. Serve a small model (examples)
llama.cpp:
  llama-server -m qwen2.5-4b-instruct.gguf --port 1234 --ctx-size 32768 -ngl 0
Ollama:
  OLLAMA_HOST=127.0.0.1:1234 ollama serve   # then: ollama pull qwen2.5:4b
Any vLLM / LM Studio server exposing POST /v1/chat/completions works.

## 2. Point the harness at it
  export LOCAL_ANALYZER_BASE_URL=http://127.0.0.1:1234/v1
  export LOCAL_ANALYZER_MODEL_ID=<exact served model name>
  export LOCAL_ANALYZER_PROVIDER=vllm   # optional, default vllm; openrouter* only for hosted
  python -m inference.framework.run --model local --game ls20 --max-actions 200 ...
  # or INFERENCE_ANALYZER_MODEL=<id> as the model-id env alias; --model <id> also works directly.

## 3. What to expect (honest)
- Plumbing: proven by CI (tests/test_analyzer_resolve.py). Requests shape: OpenAI chat completions + tools.
- Reasoning: a 4B local model tool-calls weakly. Prior 4B-lane baseline held 0 levels.
  This path tests plumbing, prompt changes (B2 pack), and harness mechanics — not miracles.
- Failure modes: connection refused = server not up; 404/"model not found" = MODEL_ID mismatch
  (must equal the string the server reports at GET /v1/models); malformed tool_calls looping =
  model too small for function calling — step up model size or reduce tool count.
- The 139K-ctx pressure of the GPU fork does not exist here; keep prompts short on small ctx windows.
