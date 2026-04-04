import type { PlatformAdapter, Capability, CapabilityResult } from '../types';
import * as fs from 'fs/promises';
import * as path from 'path';

export const claudeCodeAdapter: PlatformAdapter = {
  name: 'claude-code',

  detect(): boolean {
    return fs.existsSync(path.join(process.cwd(), '.claude'));
  },

  async install(capabilities: Capability[]): Promise<void> {
    await this.installSkills(capabilities);
    await this.installHooks();
  },

  async uninstall(capabilityNames: string[]): Promise<void> {
    for (const name of capabilityNames) {
      const skillDir = path.join(process.cwd(), '.claude', 'skills', `ai-ltc-${name}`);
      await fs.rm(skillDir, { recursive: true, force: true });
    }
    const hooksDir = path.join(process.cwd(), '.claude', 'hooks');
    await fs.rm(hooksDir, { recursive: true, force: true });
  },

  async invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    const start = Date.now();
    try {
      await this.executeSkill(name, args);
      return { status: 'success', duration: (Date.now() - start) / 1000 };
    } catch (error) {
      return { status: 'error', error: String(error), duration: (Date.now() - start) / 1000 };
    }
  },

  async listInstalled(): Promise<Capability[]> {
    const skillsDir = path.join(process.cwd(), '.claude', 'skills');
    try {
      const entries = await fs.readdir(skillsDir);
      return entries.filter(e => e.startsWith('ai-ltc-')).map(e => ({
        name: e, type: 'skill' as const, description: '', platforms: ['claude-code'],
        invoke: async () => ({ status: 'success', duration: 0 }),
      }));
    } catch {
      return [];
    }
  },

  private async installSkills(capabilities: Capability[]): Promise<void> {
    for (const cap of capabilities) {
      const skillDir = path.join(process.cwd(), '.claude', 'skills', `ai-ltc-${cap.name}`);
      await fs.mkdir(skillDir, { recursive: true });

      const skillMd = `---
name: ai-ltc-${cap.name}
description: ${cap.description}
---

# AI-LTC ${cap.name}

When the user requests ${cap.type} coordination:

1. Check current state: \`cat .ai/state.json\`
2. Determine valid transitions from current phase
3. Execute the transition and update state
4. Log to \`.ai/logs/state.log\`

## Available Phases

- \`SETUP\` — Initial context gathering
- \`EXECUTION\` — Active implementation
- \`REVIEW\` — Self-review and validation
- \`OPTIMIZER\` — Refinement and improvement
- \`CHECKPOINT\` — Save progress point
- \`DONE\` — Task complete
`;
      await fs.writeFile(path.join(skillDir, 'SKILL.md'), skillMd);
    }
  },

  private async installHooks(): Promise<void> {
    const hooksDir = path.join(process.cwd(), '.claude', 'hooks');
    await fs.mkdir(hooksDir, { recursive: true });

    const preHook = `#!/usr/bin/env bash
ai-ltc check-permission "$TOOL_NAME" "$SESSION_ID"
if [ $? -ne 0 ]; then
  echo "Permission denied by AI-LTC state machine"
  exit 1
fi
`;
    await fs.writeFile(path.join(hooksDir, 'pre-tool-use.sh'), preHook);
    await fs.chmod(path.join(hooksDir, 'pre-tool-use.sh'), 0o755);
  },

  private async executeSkill(_name: string, _args: Record<string, unknown>): Promise<void> {
    await fs.writeFile('.ai/bridge/tasks/hook-claude.json', JSON.stringify({ skill: _name, args: _args }));
  },
};
