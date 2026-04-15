# Branch Refactor Plan

## Status

- Iteration: `iter1`
- Purpose: branch semantics cleanup
- Scope: design and governance only

## Problem

The repository already behaves like a framework plus experimental lane, but the public naming still over-exposes one provider:

- `main` is stable enough to be called the framework layer
- the former `v1.5-superqwen36-preview` branch was already carrying broader experimental assets than one provider adapter

That mismatch makes the experimental lane look narrower than it really is.

## Refactor Goal

Establish a stable written distinction:

- `main` = stable framework mainline
- `Experimental` = experimental adapters, evaluation, migration scaffolding, and provider-specific work

The git branch rename is now complete; this document remains the governing rationale.

## Naming Principles

1. Use semantic names in governance documents before touching git branch names.
2. Keep the real branch name where scripts or repo metadata must match current reality.
3. Do not mix branch renaming with unrelated implementation work.

## Definitions

### `main`

Owns:

- kernel rules
- runtime templates
- promoted abstractions
- stable docs and examples

Must avoid:

- provider-specific naming as a primary abstraction
- raw experimental evidence dumps
- adapter-specific runtime heuristics

### `Experimental`

Owns:

- provider and platform adapters
- prompt migration scaffolding
- evaluation registries and dated experiment results
- experimental governance changes before promotion

Must avoid:

- silently redefining kernel truth
- bypassing promotion gates when sending work back to `main`

## Absorption Model

```text
Experimental creates evidence and candidate abstractions
-> stable review summarizes what survived
-> main absorbs the abstraction, not the whole experiment trail
```

## Promotion Gate

Experimental work may flow back into `main` only if:

1. the abstraction is no longer provider-bound
2. at least one concrete example or evidence trail exists
3. user-facing docs remain coherent for current users
4. any evaluation result used for justification is dated and attributable

## Rename Plan

### Phase 1

- use `Experimental` in governance and planning docs
- add semantic name fields where metadata benefits from it

### Phase 2

- rename the active experimental branch to `Experimental`
- update scripts, registry fields, and consumer repo references in one bounded pass

### Phase 3

- retire the provider-bound branch name from active docs
- keep historical references only where needed for git archaeology

## Deliverables For Iteration 1

- written branch semantics
- explicit promotion gate
- explicit relation between `main` and `Experimental`
- no forced git rename yet
