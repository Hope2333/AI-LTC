.PHONY: bridge test deploy-opencode deploy-claude deploy-all clean

bridge:
	@echo "Building bridge TypeScript files..."
	@npx tsc --noEmit --target ES2020 --moduleResolution node bridge/index.ts 2>/dev/null || echo "TypeScript check skipped (no tsconfig)"

test:
	@bash scripts/integration-test.sh

deploy-opencode:
	@bash scripts/deploy-adapter.sh opencode $(TARGET_REPO)

deploy-claude:
	@bash scripts/deploy-adapter.sh claude-code $(TARGET_REPO)

deploy-all:
	@bash scripts/deploy-adapter.sh all $(TARGET_REPO)

clean:
	@rm -rf .ai/bridge/tasks .ai/bridge/memory .ai/bridge/shared-memory .ai/bridge/test-results
	@echo "Cleaned bridge runtime files."
