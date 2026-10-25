# Run the 35.35 harness against YOUR models (supported path, additive only)

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
  This path tests plumbing, prompt changes (B2 pack), and harness mechanics â not miracles.
- Failure modes: connection refused = server not up; 404/"model not found" = MODEL_ID mismatch
  (must equal the string the server reports at GET /v1/models); malformed tool_calls looping =
  model too small for function calling â step up model size or reduce tool count.
- The 139K-ctx pressure of the GPU fork does not exist here; keep prompts short on small ctx windows.

## 4. Full local command (no serving boot, no GPU)
  python inference/framework/run.py --deployment-target inline --model local \
      --game ls20 --max-actions 200 --config configs/inference.json
  Required env: LOCAL_ANALYZER_BASE_URL, LOCAL_ANALYZER_MODEL_ID.
  `inline` runs games in-process; the harness never boots SGLang/vLLM here.
  Your server must implement POST /v1/chat/completions (+ optional /v1/models).

## 5. Knobs that matter for small models
- LOCAL_ANALYZER_CONTEXT_WINDOW (default 32768): lower to your server's ctx (e.g. 8192) to avoid silent truncation.
- configs/inference.json analyzer section: temperature 0.6, timeout 120, tool_timeout 30, tool_output_tokens 1024.
  On slow CPU inference raise timeout/tool_timeout (4B on CPU answers slowly; do NOT lower max_output to compensate).
- LOCAL_ANALYZER_PROVIDER: free-form. Only "openrouter"/"router" changes request shaping; everything else
  (vllm default, llamacpp, ollama, lmstudio, custom) uses the plain OpenAI shape. Set it for honest logs.
- OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_PROVIDER work as aliases (resolution order: OPENAI_* then LOCAL_*).

## 6. Backend matrix (tested shape: plain OpenAI chat completions + tools)
- llama.cpp server (--port 1234): works, tool_calls depend on model + --jinja chat template.
- Ollama (11434): works; set OLLAMA_KEEP_ALIVE to avoid reloads between games.
- vLLM / SGLang / LM Studio: native fit.
- OpenRouter: set provider=openrouter for provider pinning; needs OPENAI_API_KEY.

## 7. Report-back template (feeds the 4B baseline)
  model= / served-by= / ctx= / game= / steps= / unique= / repeats= / levels= / best_lc= / notes(tool-call quality)=
  Paste the probe-results.json harness block. Deterministic harness: every delta is code or model, never rerun noise.
