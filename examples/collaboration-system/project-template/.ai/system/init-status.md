# Init Status

Status: UNINITIALIZED
Decision: run_qwen_init
Stop Reason: STOP_REVIEW_GATE_REACHED
Next Action: Ask for the human-facing output language first, set `Status: INITING`, copy or confirm the initial skeleton, run `shared-repo-contract.prompt.md` and `qwen-init-routing.prompt.md`, answer the bounded init questionnaire, then write `.ai/system/ai-ltc-config.json` and promote the status to `INSTALLED`.

State meanings:
- `UNINITIALIZED`: init has never completed
- `INITING`: init is in progress and should be resumed if interrupted
- `INSTALLED`: AI-LTC is installed; decide between update, upgrade, or normal execution
