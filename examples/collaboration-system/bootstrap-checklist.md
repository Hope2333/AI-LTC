# Bootstrap Checklist

Use this checklist immediately after copying `project-template/` into a new repository.

## 1. Replace Project Identity

- replace placeholder repository name references in:
  - `AGENTS.md`
  - `00_HANDOFF.md`
  - `docs/ai-workbench.md`
  - `docs/ai-relay.md`
- confirm the new repository's preferred lane naming scheme
- confirm whether the repository will use one active lane or multiple registered lanes from day one

## 2. Keep Local-Only State Local

- add `.ai/` to `.gitignore` if the target repository does not already ignore it
- confirm `.omx/` or any equivalent local state directory is not committed
- do not commit copied placeholder `.ai/active-lane/*` files as if they were real project state

## 3. Rewrite Placeholder Lane State

Rewrite these files before the first real AI run:
- `00_HANDOFF.md`
- `.ai/active-lane/ai-handoff.md`
- `.ai/active-lane/current-status.md`
- `.ai/active-lane/roadmap.md`

Replace at minimum:
- placeholder lane name
- branch name
- current status
- latest commit / run placeholders
- next action placeholders
- any inherited blocker text from the template

If no escalation exists yet, clear or replace:
- `ESCALATION_REQUEST.md`

## 4. Decide The First Active Lane

Before the first execution AI run, decide:
- what the first active lane actually is
- whether the first lane is implementation, migration, packaging, i18n, or something else
- what the initial lane boundary is
- what is explicitly out of scope

If the project needs multiple lanes soon, register them in `docs/ai-relay.md` early instead of hardcoding file paths in prompts.

## 5. Verify The Protocol Layer

Check that the copied docs still agree:
- `docs/ai-relay.md`
- `docs/ai-collaboration.md`
- `docs/ai-workbench.md`
- `.ai/README.md`

Specifically confirm:
- active lane path is correct
- fixed stop phrases are present
- fixed status fields are present
- bounded-pass rule is present
- GitHub Actions first guidance is present if the target project uses CI
- v1 role split is clear:
  - GPT for architecture / optimization only
  - Qwen as default generalist operator

## 6. Adapt To The New Project's CI Reality

- if the target project has GitHub Actions, point the protocol toward the narrowest clean proof workflow
- if the target project uses another CI system, rewrite the wording so the same rule still holds: prefer the narrowest clean proof path over long local loops
- if the project has no CI yet, keep the protocol but note that local proofs are temporary until a narrow hosted proof path exists

## 7. Create The First Real Human Entry Notes

Before asking AIs to run for real, update `docs/ai-workbench.md` with:
- the actual active lane path
- the preferred prompt usage pattern for this project
- any project-specific non-commit paths or local-only directories
- any default language overrides if this project differs from the template
- whether `00_HANDOFF.md` should be treated as required during bootstrap

## 8. Do Not Copy These Blindly

Do not carry over as real facts:
- old commit IDs
- old workflow IDs
- old blockers
- old branch names
- old dependency choices
- old phase numbers if the new project does not use the same phase map

## 9. First Supervisory Pass

The first higher-cost supervisory pass should answer:
- what the active lane is
- what the next 1 to 3 actions are
- what must stay out of scope
- whether the copied protocol needs project-specific adjustment
- whether Qwen should become the default operator immediately or only after an initial GPT bootstrap pass

## 10. First Execution Pass

The first lower-cost execution pass should be small.
Good first tasks:
- verify the active lane docs are being read correctly
- confirm the working branch and latest commit
- verify the narrowest proof path
- make one bounded, low-risk change
- confirm the escalation trigger (`@ARCHITECT_HELP`) and `ESCALATION_REQUEST.md` location

## Exit Condition

This bootstrap is complete when:
- the placeholder lane files are rewritten with real project state
- the active lane is registered in `docs/ai-relay.md`
- the workbench points to the real active lane
- local-only state is confirmed non-committed
- the first supervisory and execution runs can proceed without re-explaining the system by hand
