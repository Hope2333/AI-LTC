import type { PlatformAdapter, Capability, CapabilityResult } from '../types';
import * as fs from 'fs/promises';
import * as path from 'path';

export const opencodeAdapter: PlatformAdapter = {
  name: 'opencode',

  detect(): boolean {
    return fs.existsSync(path.join(process.cwd(), '.opencode')) ||
           fs.existsSync(path.join(process.env.HOME || '', '.config', 'opencode'));
  },

  async install(capabilities: Capability[]): Promise<void> {
    const pluginDir = path.join(process.cwd(), '.opencode', 'plugins', 'ai-ltc-bridge');
    await fs.mkdir(pluginDir, { recursive: true });

    const pluginCode = this.generatePluginCode(capabilities);
    await fs.writeFile(path.join(pluginDir, 'index.js'), pluginCode);
  },

  async uninstall(capabilityNames: string[]): Promise<void> {
    const pluginDir = path.join(process.cwd(), '.opencode', 'plugins', 'ai-ltc-bridge');
    await fs.rm(pluginDir, { recursive: true, force: true });
  },

  async invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    const start = Date.now();
    try {
      await this.executeHook(name, args);
      return { status: 'success', duration: (Date.now() - start) / 1000 };
    } catch (error) {
      return { status: 'error', error: String(error), duration: (Date.now() - start) / 1000 };
    }
  },

  async listInstalled(): Promise<Capability[]> {
    const pluginDir = path.join(process.cwd(), '.opencode', 'plugins', 'ai-ltc-bridge');
    try {
      const files = await fs.readdir(pluginDir);
      return files.map(f => ({ name: f, type: 'subagent', description: '', platforms: ['opencode'], invoke: async () => ({ status: 'success', duration: 0 }) }));
    } catch {
      return [];
    }
  },

  generatePluginCode(capabilities: Capability[]): string {
    const hooks = capabilities.map(cap => `
      '${cap.type}:before:*': async (ctx) => {
        const allowed = await bridge.checkPermission(ctx.tool.name, ctx.session.id);
        if (!allowed) ctx.abort('Permission denied by AI-LTC');
      },
    `).join('\n');

    return `export default {
  name: 'ai-ltc-bridge',
  version: '1.0.0',
  hooks: {
    'session:start': async (ctx) => {
      await bridge.trigger('oml:execution:start', { sessionId: ctx.session.id, goal: ctx.project.goal });
    },
    'session:compact': async (ctx) => { await bridge.compact(ctx.session.id); },
    'session:end': async (ctx) => { await bridge.trigger('oml:done:notify', { sessionId: ctx.session.id }); },
    ${hooks}
  },
};`;
  },

  async executeHook(_name: string, _args: Record<string, unknown>): Promise<void> {
    await fs.writeFile('.ai/bridge/tasks/hook-opencode.json', JSON.stringify({ hook: _name, args: _args }));
  },
};
