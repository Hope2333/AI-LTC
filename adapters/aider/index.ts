import type { PlatformAdapter, Capability, CapabilityResult } from '../types';
import * as fs from 'fs/promises';
import * as path from 'path';

export const aiderAdapter: PlatformAdapter = {
  name: 'aider',

  detect(): boolean {
    return fs.existsSync(path.join(process.cwd(), '.aider.conf.yaml'));
  },

  async install(capabilities: Capability[]): Promise<void> {
    const configPath = path.join(process.cwd(), '.aider.conf.yaml');
    const existing = await this.readConfig(configPath);
    const commands = capabilities.map(cap => `  ai-ltc-${cap.name}:
    description: "${cap.description}"
    script: "cat /path/to/ai-ltc/.ai/state.json"`).join('\n');

    const updated = `${existing}\ncommands:\n${commands}\n`;
    await fs.writeFile(configPath, updated);
  },

  async uninstall(capabilityNames: string[]): Promise<void> {
    const configPath = path.join(process.cwd(), '.aider.conf.yaml');
    let config = await this.readConfig(configPath);
    for (const name of capabilityNames) {
      config = config.replace(new RegExp(`  ai-ltc-${name}:.*?\n`, 'gs'), '');
    }
    await fs.writeFile(configPath, config);
  },

  async invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    const start = Date.now();
    try {
      await this.executeCommand(name, args);
      return { status: 'success', duration: (Date.now() - start) / 1000 };
    } catch (error) {
      return { status: 'error', error: String(error), duration: (Date.now() - start) / 1000 };
    }
  },

  async listInstalled(): Promise<Capability[]> {
    const configPath = path.join(process.cwd(), '.aider.conf.yaml');
    try {
      const config = await this.readConfig(configPath);
      const matches = config.match(/ai-ltc-(\w+):/g) || [];
      return matches.map(m => ({
        name: m.replace('ai-ltc-', '').replace(':', ''),
        type: 'skill' as const,
        description: '',
        platforms: ['aider'],
        invoke: async () => ({ status: 'success', duration: 0 }),
      }));
    } catch {
      return [];
    }
  },

  private async readConfig(configPath: string): Promise<string> {
    try {
      return await fs.readFile(configPath, 'utf-8');
    } catch {
      return '';
    }
  },

  private async executeCommand(_name: string, _args: Record<string, unknown>): Promise<void> {
    await fs.writeFile('.ai/bridge/tasks/hook-aider.json', JSON.stringify({ command: _name, args: _args }));
  },
};
