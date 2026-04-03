# OML Plugin Adapter Guide

## Purpose

How to adapt AI-LTC capabilities for specific coding platforms (OpenCode, Claude Code, Aider, and custom platforms).

---

## 1. Adapter Architecture

Each platform adapter implements a common interface:

```typescript
interface PlatformAdapter {
  name: string;
  detect(): boolean;
  install(capabilities: Capability[]): Promise<void>;
  uninstall(capabilityNames: string[]): Promise<void>;
  invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult>;
  listInstalled(): Promise<Capability[]>;
}
```

---

## 2. OpenCode Adapter

### 2.1 Plugin Format

OpenCode uses JavaScript/TypeScript modules in `.opencode/plugins/` (project-level) or `~/.config/opencode/plugins/` (global).

```javascript
// .opencode/plugins/ai-ltc-bridge.js
export default {
  name: 'ai-ltc-bridge',
  version: '1.0.0',
  hooks: {
    'session:start': async (ctx) => {
      // Trigger AI-LTC SETUP → EXECUTION transition
      await bridge.trigger('oml:execution:start', {
        sessionId: ctx.session.id,
        goal: ctx.project.goal,
      });
    },
    'tool:before:*': async (ctx) => {
      // Intercept tool calls for permission checks
      const allowed = await bridge.checkPermission(ctx.tool.name, ctx.session.id);
      if (!allowed) {
        ctx.abort('Permission denied by AI-LTC');
      }
    },
    'session:compact': async (ctx) => {
      // Trigger context compaction
      await bridge.compact(ctx.session.id);
    },
  },
};
```

### 2.2 Installation

```bash
# Via deploy-adapter.sh
./scripts/deploy-adapter.sh opencode /path/to/target-repo

# Manual installation
cp -r adapters/opencode/bridge ~/.config/opencode/plugins/ai-ltc-bridge
```

### 2.3 Event Mapping

| OpenCode Event | AI-LTC Action |
|---------------|---------------|
| `session:start` | Trigger `oml:execution:start` |
| `session:compact` | Trigger `oml:checkpoint:create` |
| `tool:before:*` | Permission check via AI-LTC control |
| `tool:after:*` | Result logging to AI-LTC memory |
| `session:end` | Trigger `oml:done:notify` |

---

## 3. Claude Code Adapter

### 3.1 Skills Format

Claude Code uses `.claude/skills/<name>/SKILL.md` with YAML frontmatter.

```markdown
---
name: ai-ltc-state-machine
description: AI-LTC state machine coordination for structured workflows
---

# AI-LTC State Machine

When the user requests structured workflow coordination:

1. Check current state: `cat .ai/state.json`
2. Determine valid transitions from current phase
3. Execute the transition and update state
4. Log to `.ai/logs/state.log`

## Available Phases

- `SETUP` — Initial context gathering
- `EXECUTION` — Active implementation
- `REVIEW` — Self-review and validation
- `OPTIMIZER` — Refinement and improvement
- `CHECKPOINT` — Save progress point
- `DONE` — Task complete
```

### 3.2 Hooks Format

Claude Code hooks are shell commands in `.claude/hooks/`.

```bash
#!/usr/bin/env bash
# .claude/hooks/pre-tool-use.sh
# Called before every tool invocation

# Check AI-LTC permission
ai-ltc check-permission "$TOOL_NAME" "$SESSION_ID"
if [ $? -ne 0 ]; then
  echo "Permission denied by AI-LTC state machine"
  exit 1
fi
```

### 3.3 MCP Server Format

```json
// .mcp.json
{
  "mcpServers": {
    "ai-ltc-bridge": {
      "command": "node",
      "args": ["/path/to/ai-ltc/bridge/mcp-server.js"],
      "env": {
        "AI_LTC_ROOT": "/path/to/ai-ltc",
        "OML_ROOT": "/path/to/oh-my-litecode"
      }
    }
  }
}
```

### 3.4 Installation

```bash
# Via deploy-adapter.sh
./scripts/deploy-adapter.sh claude-code /path/to/target-repo

# Installs:
#   .claude/skills/ai-ltc-state-machine/SKILL.md
#   .claude/hooks/pre-tool-use.sh
#   .claude/hooks/post-tool-use.sh
#   .mcp.json (merged with existing)
```

---

## 4. Aider Adapter (Future)

### 4.1 Custom Commands

Aider doesn't have a formal plugin system. Integration happens through:

```yaml
# .aider.conf.yaml
commands:
  ai-ltc-state:
    description: "Check AI-LTC state machine status"
    script: "cat /path/to/ai-ltc/.ai/state.json"
  ai-ltc-transition:
    description: "Trigger AI-LTC phase transition"
    script: "/path/to/ai-ltc/scripts/transition.sh $1"
```

### 4.2 Limitations

- No hooks system — must rely on manual triggers
- No plugin format — capabilities are exposed as custom commands
- No MCP support — tools must be wrapped as shell commands

---

## 5. Custom Platform Adapter

### 5.1 Template

```typescript
// adapters/custom/index.ts
import type { PlatformAdapter, Capability, CapabilityResult } from '../registry';

export const customAdapter: PlatformAdapter = {
  name: 'custom',

  detect(): boolean {
    // Check for platform-specific markers
    return fs.existsSync('.custom/config.json');
  },

  async install(capabilities: Capability[]): Promise<void> {
    // Install capabilities to the custom platform
    for (const cap of capabilities) {
      await this.installCapability(cap);
    }
  },

  async uninstall(capabilityNames: string[]): Promise<void> {
    // Remove capabilities from the custom platform
    for (const name of capabilityNames) {
      await this.uninstallCapability(name);
    }
  },

  async invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    // Invoke a capability on the custom platform
    return bridge.invokeCapability(name, args);
  },

  async listInstalled(): Promise<Capability[]> {
    // List installed capabilities
    return bridge.discoverCapabilities();
  },
};
```

### 5.2 Registration

```typescript
// adapters/registry.ts
import { opencodeAdapter } from './opencode';
import { claudeCodeAdapter } from './claude-code';
import { customAdapter } from './custom';

const adapters: PlatformAdapter[] = [
  opencodeAdapter,
  claudeCodeAdapter,
  customAdapter,
];

export async function detectAdapter(): Promise<PlatformAdapter | null> {
  for (const adapter of adapters) {
    if (adapter.detect()) {
      return adapter;
    }
  }
  return null;
}
```

---

## 6. Cross-Platform Capability Matrix

| Capability | OpenCode | Claude Code | Aider | Custom |
|-----------|----------|-------------|-------|--------|
| State Machine | ✅ Plugin | ✅ Skill | ⚠️ Command | ✅ Adapter |
| Memory System | ✅ Hook | ✅ MCP | ⚠️ File | ✅ Adapter |
| Error Recovery | ✅ Hook | ✅ Hook | ❌ Manual | ✅ Adapter |
| Plugin Discovery | ✅ Native | ✅ Directory | ❌ None | ✅ Adapter |
| Session Management | ✅ Native | ✅ File | ❌ None | ✅ Adapter |
| Cross-Repo Sync | ✅ Plugin | ✅ MCP | ❌ None | ✅ Adapter |

Legend: ✅ Full support, ⚠️ Partial support, ❌ Not available
