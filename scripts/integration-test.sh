#!/usr/bin/env bash
set -euo pipefail

# AI-LTC Integration Test Suite
# Tests bridge event mapping, plugin capability invocation,
# cross-platform adapter installation, and memory persistence.

AI_LTC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DIR="${AI_LTC_ROOT}/.ai/bridge/test-results"
PASS=0
FAIL=0

pass() {
	echo "  PASS: $1"
	PASS=$((PASS + 1))
}

fail() {
	echo "  FAIL: $1"
	FAIL=$((FAIL + 1))
}

assert_file_exists() {
	local path="$1"
	local label="$2"
	if [ -f "$path" ]; then
		pass "$label exists"
	else
		fail "$label missing"
	fi
}

assert_file_contains() {
	local path="$1"
	local pattern="$2"
	local label="$3"
	if [ ! -f "$path" ]; then
		fail "$label missing source file"
	elif grep -Eq "$pattern" "$path"; then
		pass "$label"
	else
		fail "$label"
	fi
}

setup() {
	mkdir -p "$TEST_DIR"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/tasks"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/memory"
	mkdir -p "${AI_LTC_ROOT}/.ai/bridge/shared-memory"
}

test_bridge_event_mapping() {
	echo "Testing bridge event mapping..."
	local path="${AI_LTC_ROOT}/bridge/event-map.yaml"
	assert_file_exists "$path" "event-map.yaml"
	assert_file_contains "$path" "oml:execution:start" "event map includes execution start hook"
	assert_file_contains "$path" "oml:checkpoint:create" "event map includes checkpoint hook"
	assert_file_contains "$path" "memory\\.write\\(key, value\\)" "event map includes memory write mapping"
}

test_capability_registry() {
	echo "Testing capability registry..."
	local path="${AI_LTC_ROOT}/bridge/capability-registry.ts"
	assert_file_exists "$path" "capability-registry.ts"
	assert_file_contains "$path" "export interface Capability" "capability registry exports Capability"
	assert_file_contains "$path" "export class CapabilityRegistry" "capability registry exports CapabilityRegistry"
	assert_file_contains "$path" "async discoverCapabilities" "capability registry has discovery API"
}

test_protocol_spec() {
	echo "Testing protocol spec..."
	local path="${AI_LTC_ROOT}/bridge/protocol.md"
	assert_file_exists "$path" "protocol.md"
	assert_file_contains "$path" "\"taskId\"" "protocol documents taskId"
	assert_file_contains "$path" "File-based JSON" "protocol documents file-based transport"
	assert_file_contains "$path" "success\\|error\\|timeout" "protocol documents result statuses"
}

test_opencode_adapter() {
	echo "Testing OpenCode adapter..."
	local path="${AI_LTC_ROOT}/adapters/opencode/index.ts"
	assert_file_exists "$path" "opencode/index.ts"
	assert_file_contains "$path" "PlatformAdapter" "opencode adapter implements PlatformAdapter"
	assert_file_contains "$path" "async install" "opencode adapter has install API"
	assert_file_contains "$path" "async invoke" "opencode adapter has invoke API"
}

test_claude_code_adapter() {
	echo "Testing Claude Code adapter..."
	local path="${AI_LTC_ROOT}/adapters/claude-code/index.ts"
	assert_file_exists "$path" "claude-code/index.ts"
	assert_file_contains "$path" "PlatformAdapter" "claude-code adapter implements PlatformAdapter"
	assert_file_contains "$path" "async install" "claude-code adapter has install API"
	assert_file_contains "$path" "async invoke" "claude-code adapter has invoke API"
}

test_aider_adapter() {
	echo "Testing Aider adapter..."
	local path="${AI_LTC_ROOT}/adapters/aider/index.ts"
	assert_file_exists "$path" "aider/index.ts"
	assert_file_contains "$path" "PlatformAdapter" "aider adapter implements PlatformAdapter"
	assert_file_contains "$path" "async install" "aider adapter has install API"
	assert_file_contains "$path" "async invoke" "aider adapter has invoke API"
}

test_memory_persistence() {
	echo "Testing memory persistence..."
	local path="${AI_LTC_ROOT}/bridge/memory-adapter.ts"
	assert_file_exists "$path" "memory-adapter.ts"
	assert_file_contains "$path" "class MemoryAdapter" "memory adapter defines MemoryAdapter"
	assert_file_contains "$path" "async write" "memory adapter has write API"
	assert_file_contains "$path" "async read" "memory adapter has read API"
}

test_context_compaction() {
	echo "Testing context compaction..."
	local path="${AI_LTC_ROOT}/bridge/context-compact.ts"
	assert_file_exists "$path" "context-compact.ts"
	assert_file_contains "$path" "class ContextCompact" "context compaction defines ContextCompact"
	assert_file_contains "$path" "async checkUtilization" "context compaction has utilization check API"
	assert_file_contains "$path" "async compact" "context compaction has compact API"
}

test_cross_session_sharing() {
	echo "Testing cross-session sharing..."
	local path="${AI_LTC_ROOT}/bridge/cross-session.ts"
	assert_file_exists "$path" "cross-session.ts"
	assert_file_contains "$path" "class CrossSession" "cross-session sharing defines CrossSession"
	assert_file_contains "$path" "async share" "cross-session sharing has share API"
	assert_file_contains "$path" "async access" "cross-session sharing has access API"
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
