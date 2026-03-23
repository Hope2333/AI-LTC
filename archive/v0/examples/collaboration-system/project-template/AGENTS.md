# Repository AI Guidelines

## AI Relay Maintenance

Before substantial work, read `.ai/README.md`, `docs/ai-relay.md`, and then the area-specific handoff file it points to.
When using a supervisory/execution AI split, also follow `docs/ai-collaboration.md`.
After any meaningful state change, update the relevant handoff docs in the same work session so the next AI can continue without rebuilding context.

AI working-state docs and helper tools live under `.ai/` and are local-only.
Do not move them back under `docs/` unless the human explicitly asks.
Do not commit `.omx/` or `.ai/`.
