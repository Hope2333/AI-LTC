# FORMAT-STRATEGY

AI-LTC uses a mixed documentation strategy.
The goal is not to force one universal format.
The goal is to choose the cheapest format that preserves clarity, machine-readability, and long-session stability.

## Global Principles

- working language must be English
- human-facing summary language and human-input language policy should be resolved during init and stored in `.ai/system/ai-ltc-config.json`
- use plain markdown by default unless a structured format clearly provides operational value
- do not use structured formats just because they look formal
- prefer the smallest format that preserves the required semantics
- if a document must be both human-readable and machine-readable, use mixed format rather than forcing one side to lose

## Evaluation Dimensions

### Human Readability
- how easy the file is to scan and edit manually
- how well it survives long prose explanations
- whether humans can reason from it without a parser

### Token Cost
- how compact the file is when pasted into a model context
- how much punctuation overhead it adds
- how much duplication it forces in repeated keys or table headers

### Machine Parsing
- how easy it is for scripts or tools to validate and extract fields
- whether field boundaries are explicit and stable

### Diff Friendliness
- how clean git diffs remain over time
- whether a small logical change causes a large textual rewrite

### Long-Context Stability
- how robust the format is when repeatedly copied, summarized, or updated across many turns
- whether the format degrades gracefully when partially truncated or manually edited

## Format Layers

### 1. Markdown

Use for:
- human-facing explanations
- framework docs
- handoff narratives
- roadmap notes
- lane reasoning
- policies that need nuance

Strengths:
- best human readability
- good diff friendliness for prose
- good long-context stability
- low operational friction

Weaknesses:
- weak machine parsing unless conventions are very strict
- can become verbose when many stable fields are required

AI-LTC guidance:
- markdown is the default base layer
- most docs should remain markdown-first
- use headings, flat bullets, and fixed field labels when some structure is needed

### 2. YAML

Use for:
- small declarative configs
- transition rules
- workflow matrices
- settings that are hand-edited but still structured

Strengths:
- strong balance of human readability and machine parsing
- less punctuation-heavy than JSON for hand editing
- good for configuration files and state tables

Weaknesses:
- indentation-sensitive
- can become fragile in copied chat output
- nested YAML can become harder to diff and summarize cleanly

AI-LTC guidance:
- use YAML when structure is needed and humans will edit it often
- keep nesting shallow
- do not use YAML for long narrative reasoning

### 3. JSON

Use for:
- strict resolver configs
- machine-owned state
- fields that need deterministic parsing
- data exchanged with tools or scripts

Strengths:
- best machine parsing
- explicit field structure
- easy to validate

Weaknesses:
- worst human readability for nuanced content
- repeated key names increase token cost
- comments are not native

AI-LTC guidance:
- use JSON only where deterministic structure matters more than prose readability
- current example: `.ai/system/ai-ltc-config.json`
- keep JSON files shallow and small

### 4. CSV

Use for:
- flat registries
- incident indexes
- comparison tables
- dataset-like records with stable columns

Strengths:
- very compact for repeated rows
- cheap token cost for simple tabular data
- easy to diff when rows are stable

Weaknesses:
- poor for nested meaning
- weak prose support
- fragile when cells contain long text or delimiters

AI-LTC guidance:
- use CSV only for truly flat tabular material
- do not use CSV for handoff, escalation, or policy documents

### 5. Mixed Format

Use for:
- docs that need both narrative and machine-readable fields
- examples that need explanation plus structured snippets
- routing docs that combine decision logic and stable artifacts

Common pattern:
- markdown explanation
- followed by YAML/JSON snippet
- followed by a short table if comparison matters

Strengths:
- best practical compromise
- preserves human context while exposing structured anchors

Weaknesses:
- requires discipline to keep the boundary clear
- can become bloated if every section uses multiple subformats

AI-LTC guidance:
- prefer mixed format over forcing complex meaning into pure JSON or pure CSV
- use it for templates, strategy docs, and examples

## Recommended Format By Artifact Type

- framework overview docs: `Markdown`
- role prompts: `Markdown`
- handoff and escalation templates: `Markdown with fixed fields`
- resolver config: `JSON`
- init questionnaire: `Markdown`
- future workflow rules: `YAML` when they become formalized
- incident or compatibility registries: `CSV` or `Markdown table`, depending on whether narrative context matters
- strategy docs: `Mixed`

## Language Strategy

### Working Language
- always English
- use English for technical payloads, file references, commands, schema fields, and internal working notes

### Human-Facing Summary Language
- should be configured during init
- should be stored in `.ai/system/ai-ltc-config.json`
- may be Chinese, English, or another human-facing language required by the target repository owner

### Human Input Language Policy
- should be configured during init
- should tell the AI whether to expect user requests in a fixed language, multiple languages, or auto-detect mode
- should be stored in `.ai/system/ai-ltc-config.json`

### Why This Split Exists
- English is usually the most stable working language for tools, code identifiers, and prompt reuse
- human-facing summaries should follow the operator's real needs
- separating working language from summary language saves tokens and reduces ambiguity

## v2 Direction

These areas should be revisited in v2:
- quota-aware routing by model budget or Codex allocation
- compact structured state formats for long sessions
- optional YAML transition packs for state machines
- clearer criteria for when mixed format becomes too expensive
- more evidence on whether markdown+JSON or markdown+YAML is the better default hybrid for long-horizon AI work
