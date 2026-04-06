# Phase Execution Prompt Template

## Purpose

Standardized prompt template for execution agents working on a specific phase.

## Structure

```markdown
# Phase [X].[Y]: [Phase Name]

## Goal
[One sentence describing what "done" looks like]

## Context
- Current state: [where we are]
- Dependencies: [what must be done first]
- Constraints: [what we cannot change]

## Tasks
1. [Task 1] — [specific action]
2. [Task 2] — [specific action]
3. [Task 3] — [specific action]

## Verification
- [ ] Build passes (exit code 0)
- [ ] No new compile warnings
- [ ] CI green
- [ ] [Phase-specific verification]

## Guardrails
- Do not [forbidden action]
- Do not [forbidden action]
- Maintain [invariant]

## Output Format
At the end of each iteration:
- Status: [current status]
- Actions taken: [list]
- Blockers: [list]
- Next action: [specific next step]
```

## Usage

1. Copy this template to `.ai/modernization/phase-X-Y-execution.md`
2. Fill in the sections with phase-specific details
3. Reference this file in state.json `next_action`
4. Update as the phase progresses
