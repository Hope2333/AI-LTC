# AI-LTC Handoff Bundle

AI-LTC handoff is a bundle, not a single prompt. A task packet can describe a
bounded executor job, but it must be subordinate to the live `.ai` state and
the active-lane handoff files.

The active handoff surface for new AI-LTC target repositories stays inside
`.ai/`. Project `docs/` should keep long-lived project semantics, not transient
AI workflow, task-dispatch, or handoff packets.

## Required Files

Every target repository handoff should provide:

- `.ai/state.json`
- `.ai/active-lane/ai-handoff.md`
- `.ai/active-lane/status.md`
- `.ai/active-lane/current-status.md`
- `.ai/active-lane/roadmap.md`
- the current `.ai/rounds/*.md` file when the project uses rounds
- a bounded executor packet inside `.ai/`, if executor work is being dispatched

`00_HANDOFF.md` is legacy compatibility material only. Do not create it as a
new active handoff requirement.

## Source Of Truth

Use `.ai/state.json` as the canonical task-state file. Active-lane status files
should summarize the current lane and point to `.ai/state.json`; they should
not copy the full task table. Duplicated task tables drift and create false
handoff instructions.

If any supplemental handoff file conflicts with `.ai/state.json`, the state file
wins. The executor stops and reports the conflict instead of choosing between
competing instructions.

## Legal Flow

For normal delegated work, use:

```text
HANDOFF_READY -> EXECUTION -> REVIEW -> CHECKPOINT
```

- `HANDOFF_READY`: architect/chief writes the bundle.
- `EXECUTION`: executor reads the bundle and performs the bounded task.
- `REVIEW`: reviewer/chief classifies the returned evidence.
- `CHECKPOINT`: state is updated and the next lane is selected.

## Executor Packet Rules

Executor packets must:

- name the role and task;
- list read-first files;
- list allowed scope and forbidden scope;
- define required verification;
- state the completion boundary;
- state that `.ai/state.json` overrides the packet on conflict.

Executor packets must not:

- promote their own artifacts;
- unblock downstream tasks;
- override the canonical task state;
- silently widen scope when handoff files conflict.

## Project Docs Boundary

AI-LTC workflow artifacts do not belong in a target repository's project docs:

- active handoff briefs;
- executor packets;
- chief/dispatcher operating notes;
- temporary state assessments;
- round plans and review packets.

Place those files under `.ai/` instead. Keep project `docs/` for durable
project-facing contracts such as API behavior, benchmark policy, data contracts,
architecture, or operator-readable regeneration notes.
