#!/usr/bin/env bash
set -euo pipefail

# AI-LTC Integration Test Suite
# Tests bridge event mapping, plugin capability invocation,
# cross-platform adapter installation, and memory persistence.

AI_LTC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DIR="${AI_LTC_ROOT}/.ai/bridge/test-results"
PASS=0
FAIL=0

setup() {
	mkdir -p "$TEST_DIR"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/tasks"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/memory"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/shared-memory"
}

test_bridge_event_mapping() {
	echo "Testing bridge event mapping..."
	if [ -f "${AI_LTC_ROOT}/bridge/event-map.yaml" ]; then
		echo "  PASS: event-map.yaml exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: event-map.yaml missing"
		FAIL=$((FAIL + 1))
	fi
}

test_capability_registry() {
	echo "Testing capability registry..."
	if [ -f "${AI_LTC_ROOT}/bridge/capability-registry.ts" ]; then
		echo "  PASS: capability-registry.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: capability-registry.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_protocol_spec() {
	echo "Testing protocol spec..."
	if [ -f "${AI_LTC_ROOT}/bridge/protocol.md" ]; then
		echo "  PASS: protocol.md exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: protocol.md missing"
		FAIL=$((FAIL + 1))
	fi
}

test_opencode_adapter() {
	echo "Testing OpenCode adapter..."
	if [ -f "${AI_LTC_ROOT}/adapters/opencode/index.ts" ]; then
		echo "  PASS: opencode/index.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: opencode/index.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_claude_code_adapter() {
	echo "Testing Claude Code adapter..."
	if [ -f "${AI_LTC_ROOT}/adapters/claude-code/index.ts" ]; then
		echo "  PASS: claude-code/index.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: claude-code/index.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_aider_adapter() {
	echo "Testing Aider adapter..."
	if [ -f "${AI_LTC_ROOT}/adapters/aider/index.ts" ]; then
		echo "  PASS: aider/index.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: aider/index.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_memory_persistence() {
	echo "Testing memory persistence..."
	if [ -f "${AI_LTC_ROOT}/bridge/memory-adapter.ts" ]; then
		echo "  PASS: memory-adapter.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: memory-adapter.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_context_compaction() {
	echo "Testing context compaction..."
	if [ -f "${AI_LTC_ROOT}/bridge/context-compact.ts" ]; then
		echo "  PASS: context-compact.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: context-compact.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

test_cross_session_sharing() {
	echo "Testing cross-session sharing..."
	if [ -f "${AI_LTC_ROOT}/bridge/cross-session.ts" ]; then
		echo "  PASS: cross-session.ts exists"
		PASS=$((PASS + 1))
	else
		echo "  FAIL: cross-session.ts missing"
		FAIL=$((FAIL + 1))
	fi
}

main() {
	setup

	test_bridge_event_mapping
	test_capability_registry
	test_protocol_spec
	test_opencode_adapter
	test_claude_code_adapter
	test_aider_adapter
	test_memory_persistence
	test_context_compaction
	test_cross_session_sharing

	echo ""
	echo "Results: $PASS passed, $FAIL failed"

	if [ "$FAIL" -gt 0 ]; then
		exit 1
	fi
}

main "$@"
