# Collaboration System Example

This example extracts a stabilized AI collaboration protocol into a copyable project skeleton.

Current example version: `v1`

Use it when you want to bootstrap another repository with:
- a relay entrypoint
- a GPT/Qwen staged operating model
- fixed stop phrases
- fixed status fields
- local-only active lane state under `.ai/`
- GitHub Actions first for clean proof paths when available
- a handoff protocol
- an escalation protocol

## Contents

- `VERSION.md`
- `CHANGELOG.md`
- `ROLE-QUICK-REFERENCE.md`
- `install-example.md`
- `copy-into-new-repo.sh`
- `bootstrap-checklist.md`
- `project-template/AGENTS.md`
- `project-template/00_HANDOFF.md`
- `project-template/ESCALATION_REQUEST.md`
- `project-template/.ai/README.md`
- `project-template/.ai/active-lane/ai-handoff.md`
- `project-template/.ai/active-lane/current-status.md`
- `project-template/.ai/active-lane/roadmap.md`
- `project-template/docs/ai-relay.md`
- `project-template/docs/ai-collaboration.md`
- `project-template/docs/ai-workbench.md`
- `project-template/docs/templates/feature-lane-handoff.template.md`
- `project-template/docs/templates/feature-roadmap.template.md`

## How To Use

Check `VERSION.md` and `CHANGELOG.md` if you want to maintain this template as a reusable asset.

Read `install-example.md` if you want the fastest way to copy this skeleton into a new repository.

Use `bootstrap-checklist.md` before the first real AI run in the target repository.

1. Copy `project-template/` into the new repository root.
2. Rename the placeholder lane paths if needed.
3. Replace placeholder lane facts with real project facts.
4. Keep `.ai/` local-only in the target project.
5. Point prompts to `docs/ai-relay.md` instead of hardcoding lane files.
6. Use `00_HANDOFF.md` for GPT-to-Qwen transfer.
7. Use `ESCALATION_REQUEST.md` only when Qwen triggers an architecture escalation.
8. Use `ROLE-QUICK-REFERENCE.md` when you want the shortest role-selection reminder.

## What Not To Copy Blindly

- do not copy live lane state from the source project
- do not copy project-specific commit IDs, run IDs, or blockers into a new repository
- do not treat the placeholder active lane as real state; rewrite it for the target project
- do not keep the example escalation file populated if there is no real escalation yet
