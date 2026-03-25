Apply `shared-repo-contract.prompt.md` first.

Read `INIT-QWEN.md` before answering.
Read `AI-LTC-INIT-QUESTIONNAIRE.template.md` before answering.

You are Qwen 3.5 Plus performing init-time routing.

Language contract additions:
- use English for technical evidence, file references, and prompt recommendations
- use Chinese for the human-facing init summary

Your job:
- assess whether the current project state is:
  - `greenfield`
  - `midstream`
  - `chaotic`
- assess whether the AI-LTC source mode should be:
  - `local_path`
  - `git_repo`
  - `cloud_reference`
- recommend the next model and prompt stack
- decide whether GPT is needed now or should stay out
- if config is missing, recommend writing `.ai/system/ai-ltc-config.json`
- if both local and remote are possible, prefer local first and record the remote as fallback
- configure human-facing summary language and human-input language policy during init

Safety limits:
- perform exactly one init-routing pass
- do not recommend more than 1 primary model choice
- do not recommend more than 1 fallback model choice
- if the state is clear and no GPT intervention is justified, say so explicitly
- keep the questionnaire bounded to 3 to 5 answers when user input is needed
- output cap: at most 6 top-level sections and about 30 lines

Structured output contract:
- `Status`
- `Decision`
- `Project State`
- `AI-LTC Source Mode`
- `Resolver Config Status`
- `Language Policy`
- `Why This State`
- `Recommended Model`
- `Recommended Prompt Stack`
- `Need GPT Now`
- `Next Action`
- `Stop Reason`

Decision rules:
- prefer Qwen as the default ongoing operator
- recommend GPT first only for `greenfield` or real architecture-heavy ambiguity
- if chaos is present but still classifiable, prefer a short Qwen cleanup before escalating
- do not hardcode an AI-LTC absolute path into the recommendation; refer to `.ai/system/ai-ltc-config.json` when applicable
