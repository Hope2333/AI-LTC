#!/usr/bin/env bash
set -euo pipefail

# Deploy AI-LTC bridge adapter to target platform
# Usage: deploy-adapter.sh <platform> <target-repo>
#   platform: opencode | claude-code | aider | all
#   target-repo: path to the target repository

AI_LTC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLATFORM="${1:-}"
TARGET_REPO="${2:-}"

if [ -z "$PLATFORM" ] || [ -z "$TARGET_REPO" ]; then
	echo "Usage: $0 <platform> <target-repo>"
	echo "  platform: opencode | claude-code | aider | all"
	echo "  target-repo: path to the target repository"
	exit 1
fi

if [ ! -d "$TARGET_REPO" ]; then
	echo "Error: Target repository does not exist: $TARGET_REPO"
	exit 1
fi

deploy_opencode() {
	local target="$1"
	local plugin_dir="${target}/.opencode/plugins/ai-ltc-bridge"
	mkdir -p "$plugin_dir"
	cp "${AI_LTC_ROOT}/adapters/opencode/index.ts" "${plugin_dir}/index.ts"
	echo "Deployed OpenCode adapter to ${plugin_dir}"
}

deploy_claude_code() {
	local target="$1"
	local skills_dir="${target}/.claude/skills"
	local hooks_dir="${target}/.claude/hooks"

	mkdir -p "${skills_dir}/ai-ltc-state-machine"
	cat >"${skills_dir}/ai-ltc-state-machine/SKILL.md" <<'EOF'
---
name: ai-ltc-state-machine
description: AI-LTC state machine coordination for structured workflows
---

# AI-LTC State Machine

1. Check current state: `cat .ai/state.json`
2. Determine valid transitions from current phase
3. Execute the transition and update state
4. Log to `.ai/logs/state.log`
EOF

	mkdir -p "$hooks_dir"
	cat >"${hooks_dir}/pre-tool-use.sh" <<'EOF'
#!/usr/bin/env bash
ai-ltc check-permission "$TOOL_NAME" "$SESSION_ID"
if [ $? -ne 0 ]; then
  echo "Permission denied by AI-LTC state machine"
  exit 1
fi
EOF
	chmod +x "${hooks_dir}/pre-tool-use.sh"

	echo "Deployed Claude Code adapter to ${target}"
}

deploy_aider() {
	local target="$1"
	local config="${target}/.aider.conf.yaml"

	cat >>"$config" <<EOF

commands:
  ai-ltc-state:
    description: "Check AI-LTC state machine status"
    script: "cat ${AI_LTC_ROOT}/.ai/state.json"
  ai-ltc-transition:
    description: "Trigger AI-LTC phase transition"
    script: "${AI_LTC_ROOT}/scripts/transition.sh \$1"
EOF

	echo "Deployed Aider adapter to ${target}"
}

case "$PLATFORM" in
opencode)
	deploy_opencode "$TARGET_REPO"
	;;
claude-code)
	deploy_claude_code "$TARGET_REPO"
	;;
aider)
	deploy_aider "$TARGET_REPO"
	;;
all)
	deploy_opencode "$TARGET_REPO"
	deploy_claude_code "$TARGET_REPO"
	deploy_aider "$TARGET_REPO"
	;;
*)
	echo "Error: Unknown platform: $PLATFORM"
	echo "Supported: opencode, claude-code, aider, all"
	exit 1
	;;
esac
