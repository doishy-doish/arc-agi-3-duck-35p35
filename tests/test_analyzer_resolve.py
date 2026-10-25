import os, sys
sys.path.insert(0, "src-patched/ARC3-Inference")
from inference.agent.tool_agent import _resolve_analyzer_model
os.environ["LOCAL_ANALYZER_BASE_URL"] = "http://127.0.0.1:1234/v1"
os.environ["LOCAL_ANALYZER_MODEL_ID"] = "test-4b"
os.environ.pop("OPENAI_BASE_URL", None)
c = _resolve_analyzer_model("local")
assert c.base_url == "http://127.0.0.1:1234/v1", c
assert c.model_id == "test-4b", c
c2 = _resolve_analyzer_model("qwen-local")
assert c2.model_id == "test-4b", c2
os.environ["OPENAI_BASE_URL"] = "http://10.0.0.9:8080/v1"
c3 = _resolve_analyzer_model("custom-id")
assert c3.base_url == "http://10.0.0.9:8080/v1" and c3.model_id == "custom-id", c3
saved = os.environ.pop("LOCAL_ANALYZER_MODEL_ID")
os.environ.pop("INFERENCE_ANALYZER_MODEL", None)
try:
    _resolve_analyzer_model("")
    raise SystemExit("expected ValueError for missing model id")
except ValueError:
    pass
finally:
    os.environ["LOCAL_ANALYZER_MODEL_ID"] = saved
print("analyzer-resolve OK: local preset, alias preset, direct id, missing-id error")

import importlib
os.environ["LOCAL_ANALYZER_PROVIDER"] = "llamacpp"
os.environ["OPENAI_BASE_URL"] = "http://10.0.0.9:8080/v1"
c4 = _resolve_analyzer_model("custom-id")
assert c4.base_url == "http://10.0.0.9:8080/v1" and c4.model_id == "custom-id", c4
assert c4.provider == "llamacpp", c4
print("provider-passthrough OK: custom provider preserved, OPENAI_* alias route works")
