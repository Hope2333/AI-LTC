# Home AI Consumer Framework

## Status

- Lane: `Experimental`
- Date: 2026-04-16
- Scope: Home-level `.ai` consumption framework exploration
- Runtime body: OML
- First external substrate: OpenClaw on Arch

## Purpose

Explore how AI-LTC can coordinate a personal, home-machine AI stack without becoming the runtime itself.

The framework target is a reusable `.ai` consumption layer for local projects and personal automation. It should let a user install execution bodies such as OML and OpenClaw while AI-LTC keeps the policy, state, memory, recovery, and evaluation rules stable.

## Working Thesis

Home-level AI needs three layers:

| Layer | Owner | Responsibility |
|---|---|---|
| Brain | AI-LTC | state machine, role policy, memory interpretation, recovery rules |
| Body | OML | adapters, hooks, MCP, session control, worker lifecycle, execution evidence |
| Substrate | OpenClaw and other tools | concrete local automation capabilities |

AI-LTC should decide whether a task is allowed, staged, reviewed, or blocked. OML should run and observe. OpenClaw should perform only the concrete automation delegated to it.

## Consumer Framework Shape

A Home-level `.ai` installation should contain:

| Area | Example | Purpose |
|---|---|---|
| state | `.ai/state.json` | current phase, task queue, blockers |
| policy | `.ai/system/ai-ltc-config.json` | model and runtime routing |
| memory | `.ai/memories/*.md` | persistent user, project, and feedback context |
| evidence | `.ai/evidence/*.jsonl` | runtime observations captured by OML |
| evaluation | `.ai/evaluation/*.yaml` | local experimental outcomes before framework promotion |
| handoff | `.ai/active-lane/*.md` | current local operating lane |

The framework repository should provide templates and validation rules. It should not own each consumer machine's private runtime data.

## OpenClaw As First Substrate

OpenClaw is useful for this exploration because it is a broad local agent substrate rather than a narrow coding CLI. That makes it a good pressure test for AI-LTC boundaries.

Initial OpenClaw assumptions:

- install via Arch/AUR when available for system consistency
- prefer `openclaw-agent-bwrap` for early Home-level experiments
- treat direct `openclaw` execution as high-risk until evidence proves a narrower trust model
- capture `openclaw doctor` output as runtime evidence, not as policy truth

## Risk Tiers

| Tier | Description | Default Handling |
|---|---|---|
| H0 inspect | version, help, doctor, static config reads | allowed |
| H1 local sandbox | file-limited task in fake home or restricted workspace | allowed after OML evidence capture exists |
| H2 project write | writes inside a selected project repo | requires AI-LTC phase gate and review |
| H3 personal data | reads or writes broad home data, messages, accounts, browsers | blocked until explicit human approval model exists |
| H4 external actuation | sends messages, purchases, posts, deletes cloud data | blocked for this exploration |

## Experimental Questions

1. Can AI-LTC express Home-level policy without hardcoding OpenClaw-specific behavior?
2. Can OML capture enough evidence from OpenClaw runs to support later AI-LTC evaluation?
3. Can bubblewrap-style fake-home execution become the default consumer safety posture?
4. Can `.ai` remain portable across coding projects and personal automation projects?
5. Which OpenClaw capabilities belong behind explicit approval rather than automatic routing?

## Iteration 0 Acceptance Criteria

- OpenClaw is installed on the Arch workstation through a system-visible channel.
- OML records the installation path, wrapper commands, and evidence schema.
- AI-LTC Experimental records risk tiers and the Home-level framework shape.
- No broad personal-data or external-actuation task is enabled by default.
- A later adapter implementation can be scoped to detection, health, sandbox planning, and evidence capture before task dispatch.

## Promotion Rule

Nothing from this document should move to `main` until there is:

- one OML adapter slice or executable check
- one dated evaluation record
- one documented blocked-risk case
- one successful sandboxed local task with captured evidence

Until then, this remains an Experimental consumer-framework exploration.
