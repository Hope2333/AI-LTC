# AI-LTC Init Questionnaire Template

Purpose:
- use this bounded intake when Qwen is initializing AI-LTC in a target repository
- keep the intake small and structured
- use the answers to populate `.ai/system/ai-ltc-config.json`

Question cap:
- ask at most 5 answers
- prefer 3 to 4 when possible

Suggested questions:
1. `AI-LTC Source Mode`
- `local_path`
- `git_repo`
- `cloud_reference`

2. `AI-LTC Location`
- if `local_path`: local root path
- if `git_repo`: repo URL and ref
- if `cloud_reference`: canonical URL or mirror identifier

3. `Remote Fallback And Refresh Policy`
- remote repo URL or cloud reference
- whether Qwen may refresh the local checkout when needed

4. `Project State`
- `greenfield`
- `midstream`
- `chaotic`

5. `Default Operator Model And GPT Bootstrap Need`
- usually `qwen-3.5-plus`
- whether GPT bootstrap is needed now

Writeback rule:
- after the questionnaire, write one resolver config file:
  - `.ai/system/ai-ltc-config.json`
- do not scatter raw source paths across multiple `.ai` docs
- lane docs may say `Resolver: .ai/system/ai-ltc-config.json`
