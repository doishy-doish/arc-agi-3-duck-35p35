# arc-agi-3-duck-35p35 — public solution repo (ARC Prize 2026, ARC-AGI-3)

Provenance: Tufa Labs Duck harness (Tufalabs/duck-harness @ 7652836) -> sirikilohit 35.35 notebook
(attached source bundle = unchanged Tufa snapshot; all modifications in the notebook setup patch) ->
this repo (notebook + extracted patch + patched tree + local-model path + CI).

## Contents
- `the-agi-boys-i-am-better.ipynb` — the 35.35 notebook, verbatim (Kaggle submit path, RTX PRO 6000, internet OFF).
- `harness.patch` — the notebook setup patch (cell 2), extracted. Applies to the Tufa snapshot (verified 16/16 files, CPU-checked in CI).
- `src-patched/` — the patched tree (10 modified + 6 new files), materialized for review and for building tomorrow's diffs (B2 prompt pack).
- `LOCAL_MODELS.md` — run the SAME harness against local / small models over any OpenAI-compatible endpoint (llama.cpp, Ollama, vLLM, LM Studio). Additive only: default path unchanged.
- `.env.example` — the four env vars for the local path.
- `B2-ON-35.35-DRAFT.md` — tomorrow's prompt-pack proposal (probe-first + goal-as-procedure + read-transition-frames).
- `tests/` + `.github/workflows/cpu-checks.yml` — CPU CI: patch applies, everything compiles, analyzer model resolution works.

## Model weights / datasets
Not redistributed here. Kaggle run attaches: pennyroyal-v253, taaf-kaggle-source-bundle-copy,
intel-qwen3.8-flash-next-w4a16-autoround, albucino-qwen3-8-flash-next-drafter, sglang-penny-build-qwen
(Pennyroyal fork @2c675da, MTP spec-decode capable). Local path: bring your own GGUF / Ollama model.

## License / credit
Harness: Tufa Labs / ARC Prize. Notebook + fork modifications: sirikilohit (35.35).
Local-model docs, CI, B2 draft: this repo. Upstream harness license: none-field.
Full credit to Jeroen Cottaar and the Tufa Labs team for the Duck solver and harness.
