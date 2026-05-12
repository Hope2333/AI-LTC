# Local AI Workspace

This directory stores active AI handoff, status, and roadmap files for the current local workspace.

- It is intentionally local-only.
- It should not be committed.
- Project `docs/` should stay reserved for durable project documentation.
- AI-LTC workflow, handoff, executor packet, round, and temporary state docs stay under `.ai/`.
- `.ai/state.json` is the first-order task state.
- Qwen is the default ongoing operator in the v1 framework.
- GPT should usually appear only for bootstrap architecture or explicit escalations.
- AI-LTC source resolution should be centralized under `.ai/system/ai-ltc-config.json`.
- Prefer a local AI-LTC checkout first and keep a remote fallback recorded in the resolver.
- Do not hardcode the framework root path into multiple `.ai` docs.
