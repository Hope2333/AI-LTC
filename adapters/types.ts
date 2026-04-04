export interface CapabilityResult {
  status: 'success' | 'error' | 'timeout';
  data?: unknown;
  error?: string;
  duration: number;
}

export interface Capability {
  name: string;
  type: 'agent' | 'subagent' | 'mcp' | 'skill';
  description: string;
  platforms: string[];
  invoke(args: Record<string, unknown>): Promise<CapabilityResult>;
}

export interface PlatformAdapter {
  name: string;
  detect(): boolean;
  install(capabilities: Capability[]): Promise<void>;
  uninstall(capabilityNames: string[]): Promise<void>;
  invoke(name: string, args: Record<string, unknown>): Promise<CapabilityResult>;
  listInstalled(): Promise<Capability[]>;
}
