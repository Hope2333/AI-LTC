# Changelog

## 1.0.0

Upgraded the collaboration-system example to the AI-LTC v1 framework.

Added:
- `project-template/00_HANDOFF.md`
- `project-template/ESCALATION_REQUEST.md`
- GPT bootstrap / Qwen default / GPT optimizer role model
- handoff protocol and escalation protocol wording
- self-evolving docs rule in the template-level protocol docs

Changed:
- example README and bootstrap docs now describe Qwen as the default ongoing operator
- copied project template docs now describe GPT as architecture/optimization-only by default
- install flow now includes `00_HANDOFF.md` and `ESCALATION_REQUEST.md`

## 0.1.0

Initial extracted reusable collaboration-system example.

Included:
- `project-template/` skeleton for cross-project reuse
- local-only `.ai/` active lane scaffold
- `docs/ai-relay.md`, `docs/ai-collaboration.md`, and `docs/ai-workbench.md` example copies
- feature lane handoff and roadmap templates
- `bootstrap-checklist.md`
- `install-example.md`
- `copy-into-new-repo.sh`
- fixed stop phrases and fixed status fields in the reusable protocol layer
