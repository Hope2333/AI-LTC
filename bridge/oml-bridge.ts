import { CapabilityRegistry, type Capability, type CapabilityResult } from './capability-registry';

export class BridgeError extends Error {
  constructor(
    public code: 'OML_UNAVAILABLE' | 'CAPABILITY_NOT_FOUND' | 'TASK_TIMEOUT' | 'PROTOCOL_ERROR',
    public details: string,
    public recoverable: boolean
  ) {
    super(`[Bridge] ${code}: ${details}`);
  }
}

interface TaskPayload {
  taskId: string;
  type: 'subagent' | 'skill' | 'mcp';
  capability: string;
  payload: {
    description: string;
    scope?: string;
    timeout?: number;
  };
  metadata: {
    sessionId: string;
    phase: string;
    priority: number;
  };
}

interface TaskResult {
  taskId: string;
  status: 'success' | 'error' | 'timeout';
  result?: {
    findings?: string[];
    context?: string;
  };
  error?: string;
  duration: number;
  workerId?: string;
}

interface EventMapping {
  transition: string;
  hook: string;
  payloadSchema: Record<string, string>;
}

export class OmlBridge {
  private registry: CapabilityRegistry;
  private eventMap: EventMapping[];
  private omlAvailable: boolean;

  constructor() {
    this.registry = new CapabilityRegistry();
    this.eventMap = [];
    this.omlAvailable = true;
  }

  async initialize(): Promise<void> {
    await this.loadEventMap();
    await this.registry.discoverCapabilities();
  }

  private async loadEventMap(): Promise<void> {
    this.eventMap = [
      { transition: 'SETUP → EXECUTION', hook: 'oml:execution:start', payloadSchema: { sessionId: 'string', goal: 'string', tasks: 'array' } },
      { transition: 'EXECUTION → REVIEW', hook: 'oml:review:start', payloadSchema: { sessionId: 'string', phase: 'string', artifacts: 'array' } },
      { transition: 'REVIEW → OPTIMIZER', hook: 'oml:optimize:start', payloadSchema: { sessionId: 'string', reviewFindings: 'object' } },
      { transition: 'OPTIMIZER → CHECKPOINT', hook: 'oml:checkpoint:create', payloadSchema: { sessionId: 'string', summary: 'string', metrics: 'object' } },
      { transition: 'Any → BLOCKED', hook: 'oml:blocked:notify', payloadSchema: { sessionId: 'string', blocker: 'string', context: 'object' } },
      { transition: 'BLOCKED → EXECUTION', hook: 'oml:blocked:resolve', payloadSchema: { sessionId: 'string', resolution: 'string' } },
      { transition: 'Any → DONE', hook: 'oml:done:notify', payloadSchema: { sessionId: 'string', finalSummary: 'string' } },
    ];
  }

  async triggerHook(transition: string, payload: Record<string, unknown>): Promise<void> {
    const mapping = this.eventMap.find(e => {
      if (e.transition === transition) return true;
      const [from, to] = e.transition.split(' → ');
      if (from === 'Any' && transition.endsWith(to)) return true;
      return false;
    });

    if (!mapping) {
      throw new BridgeError('PROTOCOL_ERROR', `No hook mapping for transition: ${transition}`, false);
    }

    await this.invokeHook(mapping.hook, payload);
  }

  private async invokeHook(hookName: string, payload: Record<string, unknown>): Promise<void> {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        if (!this.omlAvailable) {
          throw new BridgeError('OML_UNAVAILABLE', 'OML runtime not available', true);
        }

        await this.executeHook(hookName, payload);
        return;
      } catch (error) {
        if (attempt === 3) {
          throw new BridgeError('OML_UNAVAILABLE', `Hook ${hookName} failed after 3 retries: ${error}`, false);
        }
        await this.delay(1000 * attempt);
      }
    }
  }

  private async executeHook(_hookName: string, _payload: Record<string, unknown>): Promise<void> {
    await this.writeTaskFile(`hook-${Date.now()}`, {
      type: 'hook',
      payload: _payload,
    });
  }

  async dispatchTask(task: TaskPayload): Promise<string> {
    const capability = this.registry.getCapability(task.capability);
    if (!capability) {
      await this.registry.discoverCapabilities();
      const retry = this.registry.getCapability(task.capability);
      if (!retry) {
        throw new BridgeError('CAPABILITY_NOT_FOUND', `Capability not found: ${task.capability}`, false);
      }
    }

    await this.writeTaskFile(task.taskId, task);
    return task.taskId;
  }

  async collectResult(taskId: string): Promise<TaskResult> {
    const taskFile = `.ai/bridge/tasks/${taskId}.json`;
    try {
      const content = await this.readTaskFile(taskFile);
      if (!content) {
        throw new BridgeError('TASK_TIMEOUT', `No result file for task: ${taskId}`, true);
      }
      return JSON.parse(content) as TaskResult;
    } catch (error) {
      throw new BridgeError('PROTOCOL_ERROR', `Failed to read result for task ${taskId}: ${error}`, true);
    }
  }

  async loadCapability(name: string): Promise<Capability | undefined> {
    return this.registry.loadCapability(name);
  }

  async listCapabilities(): Promise<Capability[]> {
    return this.registry.listCapabilities();
  }

  async invokeCapability(name: string, args: Record<string, unknown>): Promise<CapabilityResult> {
    const capability = this.registry.getCapability(name);
    if (!capability) {
      throw new BridgeError('CAPABILITY_NOT_FOUND', `Capability not found: ${name}`, false);
    }
    return capability.invoke(args);
  }

  private async writeTaskFile(taskId: string, data: unknown): Promise<void> {
    const fs = await import('fs/promises');
    const path = await import('path');
    const taskDir = '.ai/bridge/tasks';
    await fs.mkdir(path.join(process.cwd(), taskDir), { recursive: true });
    const filePath = path.join(process.cwd(), taskDir, `${taskId}.json`);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
  }

  private async readTaskFile(filePath: string): Promise<string | null> {
    const fs = await import('fs/promises');
    try {
      return await fs.readFile(filePath, 'utf-8');
    } catch {
      return null;
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
