# TOOLS

AI-LTC now includes a small tooling layer for validating and summarizing target-repository state.
These tools are intentionally narrow.
They do not replace the framework docs.
They make the framework easier to validate and reuse.

## Tool List

### 1. `scripts/init_validator.py`

Purpose:
- validate `.ai/system/init-status.md`

Checks:
- required status fields exist
- init status value is valid
- installed-state logic is coherent enough for the current repository

Typical usage:

```sh
python3 scripts/init_validator.py /path/to/target-repo
```

### 2. `scripts/resolver_validator.py`

Purpose:
- validate `.ai/system/ai-ltc-config.json`

Checks:
- required resolver keys exist
- source mode is valid
- working language is `English`
- summary/input language policy exists

Typical usage:

```sh
python3 scripts/resolver_validator.py /path/to/target-repo
```

### 3. `scripts/upgrade_validator.py`

Purpose:
- classify a target repository into:
  - `Fresh Init`
  - `Resume Init`
  - `Update`
  - `Upgrade`
  - `Normal Execution`

Checks:
- init status is parseable
- resolver config is coherent enough for classification
- current and target version can be compared

Typical usage:

```sh
python3 scripts/upgrade_validator.py /path/to/target-repo --target-version v1.8.1
```

### 4. `scripts/state_pack_generator.py`

Purpose:
- generate a compact markdown state snapshot for a target repository

Output includes:
- init state
- framework version
- source mode
- language policy
- active-lane presence
- handoff/escalation presence

Typical usage:

```sh
python3 scripts/state_pack_generator.py /path/to/target-repo
python3 scripts/state_pack_generator.py /path/to/target-repo --output /tmp/state-pack.md
```

### 5. `scripts/state_pack_validator.py`

Purpose:
- validate the compact state-pack structure
- ensure generated or edited state packs still contain the minimum operational fields

Typical usage:

```sh
python3 scripts/state_pack_validator.py /path/to/state-pack.md
```

## Recommended Order

For a target repository:

1. `init_validator.py`
2. `resolver_validator.py`
3. `upgrade_validator.py`
4. `state_pack_generator.py`
5. `state_pack_validator.py`

## Operating Principle

- validators should fail on broken structure
- validators may warn on expected template conditions
- generators should stay compact
- all working payloads should remain English-friendly and machine-readable enough for reuse

## Release Discipline

- new tooling should land on the `v1.x` or `v2.0.0-rcX` line before being treated as stable
- `v2.0.0` should come only after the tooling layer has real-repository validation, not just template validation
