# Collaboration System Template Version

- Template name: `collaboration-system`
- Current version: `0.1.0`
- Status: `active`
- Compatibility note: derived from the stabilized AI collaboration protocol in `/home/miao/develop/enve`

## Versioning Rule

Increment:
- patch when wording, examples, or docs clarity improves without changing the protocol contract
- minor when prompts, fields, stop phrases, or template structure change in a backward-compatible way
- major when the expected directory layout, required fields, or protocol semantics change incompatibly

## Current Contract Highlights

- fixed stop phrases
- fixed status fields
- bounded-pass rule
- GitHub Actions first for narrow clean proof paths when available
- local-only active state under `.ai/`
