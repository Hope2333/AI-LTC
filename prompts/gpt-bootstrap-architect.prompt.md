Compatibility entrypoint for the legacy bootstrap architect prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/roles/architect.prompt.md`.
Apply `prompts/phases/init.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the role and phase prompts directly.

Required behavior:
- design the initial structure without becoming the long-running operator
- define the file-system skeleton, lane entrypoints, and initial working boundaries
- prefer a clean, minimal system over speculative completeness
- create or refresh `00_HANDOFF.md`
- exit after the architecture handoff is ready

Structured output contract:
- `Status`
- `Decision`
- `Architecture Summary`
- `Initial Lane Setup`
- `Immediate Next Actions For Generalist`
- `Risks`
- `Docs Updated`
- `Stop Reason`
