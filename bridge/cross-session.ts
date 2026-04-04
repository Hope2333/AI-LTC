import * as fs from 'fs/promises';
import * as path from 'path';

interface SharedKnowledge {
  key: string;
  value: unknown;
  sourceSession: string;
  timestamp: number;
  accessedBy: string[];
}

export class CrossSession {
  private sharedDir: string;

  constructor(sharedDir = '.ai/bridge/shared-memory') {
    this.sharedDir = sharedDir;
  }

  async share(sessionId: string, key: string, value: unknown): Promise<void> {
    await this.ensureSharedDir();
    const entry: SharedKnowledge = {
      key,
      value,
      sourceSession: sessionId,
      timestamp: Date.now(),
      accessedBy: [sessionId],
    };
    const filePath = path.join(this.sharedDir, `${key}.json`);
    await fs.writeFile(filePath, JSON.stringify(entry));
  }

  async access(sessionId: string, key: string): Promise<unknown | null> {
    const filePath = path.join(this.sharedDir, `${key}.json`);
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const entry = JSON.parse(content) as SharedKnowledge;
      if (!entry.accessedBy.includes(sessionId)) {
        entry.accessedBy.push(sessionId);
        await fs.writeFile(filePath, JSON.stringify(entry));
      }
      return entry.value;
    } catch {
      return null;
    }
  }

  async find(sessionId: string, pattern: string): Promise<SharedKnowledge[]> {
    await this.ensureSharedDir();
    const files = await fs.readdir(this.sharedDir);
    const results: SharedKnowledge[] = [];

    for (const file of files) {
      if (file.includes(pattern)) {
        const content = await fs.readFile(path.join(this.sharedDir, file), 'utf-8');
        results.push(JSON.parse(content) as SharedKnowledge);
      }
    }

    return results;
  }

  async clear(key: string): Promise<void> {
    const filePath = path.join(this.sharedDir, `${key}.json`);
    await fs.rm(filePath, { force: true });
  }

  private async ensureSharedDir(): Promise<void> {
    await fs.mkdir(this.sharedDir, { recursive: true });
  }
}
