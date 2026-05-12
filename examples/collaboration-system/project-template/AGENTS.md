# Repository AI Guidelines

## AI Relay Maintenance

Before substantial work, read `.ai/README.md`, `.ai/protocols/ai-relay.md`, and then the area-specific handoff file it points to.
When using a supervisory/execution AI split, also follow `.ai/protocols/ai-collaboration.md`.
After any meaningful state change, update the relevant handoff docs in the same work session so the next AI can continue without rebuilding context.

## v1 Role Model

- Architect and optimizer roles should not be the always-on operators by default.
- Use architect and optimizer roles mainly for:
  - initial architecture/bootstrap
  - explicit optimization, audit, or escalation handling
- Use the generalist role as the default operator for ongoing supervision and execution.
- When the architect role hands off to the generalist role, update `.ai/state.json` first and keep supplemental handoff docs under `.ai/`.
- When the generalist role hits repeated failure or architecture deadlock, trigger `@ARCHITECT_HELP` and write `ESCALATION_REQUEST.md`.
- When the project is a fresh deployment or a `v0 -> v1` upgrade, run init and maintain `.ai/system/ai-ltc-config.json`.

AI working-state docs and helper tools live under `.ai/` and are local-only.
Do not move AI-LTC workflow, handoff, packet, round, or temporary state docs back under `docs/`.
Do not commit `.omx/` or `.ai/`.
