import type { PlatformAdapter, Capability, CapabilityResult } from './types';
import { opencodeAdapter } from './opencode';
import { claudeCodeAdapter } from './claude-code';
import { aiderAdapter } from './aider';

const adapters: PlatformAdapter[] = [
  opencodeAdapter,
  claudeCodeAdapter,
  aiderAdapter,
];

export async function detectAdapter(): Promise<PlatformAdapter | null> {
  for (const adapter of adapters) {
    if (adapter.detect()) {
      return adapter;
    }
  }
  return null;
}

export async function installCapabilities(adapter: PlatformAdapter, capabilities: Capability[]): Promise<void> {
  await adapter.install(capabilities);
}

export async function uninstallCapabilities(adapter: PlatformAdapter, capabilityNames: string[]): Promise<void> {
  await adapter.uninstall(capabilityNames);
}

export { opencodeAdapter, claudeCodeAdapter, aiderAdapter };
