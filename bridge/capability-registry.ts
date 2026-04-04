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

interface CapabilityMetadata {
  name: string;
  type: string;
  description: string;
  platforms: string[];
}

export class CapabilityRegistry {
  private metadata: Map<string, CapabilityMetadata>;
  private loaded: Map<string, Capability>;

  constructor() {
    this.metadata = new Map();
    this.loaded = new Map();
  }

  async discoverCapabilities(): Promise<Capability[]> {
    const plugins = await this.listPlugins();
    const capabilities: Capability[] = [];

    for (const plugin of plugins) {
      const meta: CapabilityMetadata = {
        name: plugin.name,
        type: plugin.type,
        description: plugin.description,
        platforms: plugin.platforms || ['opencode', 'claude-code'],
      };
      this.metadata.set(plugin.name, meta);

      capabilities.push({
        name: plugin.name,
        type: plugin.type as Capability['type'],
        description: plugin.description,
        platforms: meta.platforms,
        invoke: (args) => this.invokePlugin(plugin.name, args),
      });
    }

    return capabilities;
  }

  getCapability(name: string): Capability | undefined {
    const meta = this.metadata.get(name);
    if (!meta) return undefined;

    const loaded = this.loaded.get(name);
    if (loaded) return loaded;

    return {
      name: meta.name,
      type: meta.type as Capability['type'],
      description: meta.description,
      platforms: meta.platforms,
      invoke: (args) => this.invokePlugin(name, args),
    };
  }

  async loadCapability(name: string): Promise<Capability | undefined> {
    const meta = this.metadata.get(name);
    if (!meta) return undefined;

    if (this.loaded.has(name)) {
      return this.loaded.get(name);
    }

    const capability: Capability = {
      name: meta.name,
      type: meta.type as Capability['type'],
      description: meta.description,
      platforms: meta.platforms,
      invoke: (args) => this.invokePlugin(name, args),
    };

    this.loaded.set(name, capability);
    return capability;
  }

  listCapabilities(): Capability[] {
    const capabilities: Capability[] = [];
    for (const [name, meta] of this.metadata) {
      capabilities.push({
        name,
        type: meta.type as Capability['type'],
        description: meta.description,
        platforms: meta.platforms,
        invoke: (args) => this.invokePlugin(name, args),
      });
    }
    return capabilities;
  }

  private async listPlugins(): Promise<Array<{ name: string; type: string; description: string; platforms?: string[] }>> {
    return [];
  }

  private async invokePlugin(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    const start = Date.now();
    try {
      return {
        status: 'success',
        data: null,
        duration: (Date.now() - start) / 1000,
      };
    } catch (error) {
      return {
        status: 'error',
        error: String(error),
        duration: (Date.now() - start) / 1000,
      };
    }
  }
}
