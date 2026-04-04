import * as fs from 'fs/promises';
import * as path from 'path';

interface MemoryEntry {
  key: string;
  value: unknown;
  sessionId: string;
  timestamp: number;
}

export class MemoryAdapter {
  private storageDir: string;

  constructor(storageDir = '.ai/bridge/memory') {
    this.storageDir = storageDir;
  }

  async write(sessionId: string, key: string, value: unknown): Promise<void> {
    await this.ensureStorageDir();
    const entry: MemoryEntry = { key, value, sessionId, timestamp: Date.now() };
    const filePath = this.getMemoryFilePath(sessionId, key);
    await fs.writeFile(filePath, JSON.stringify(entry));
  }

  async read(sessionId: string, key: string): Promise<unknown | null> {
    const filePath = this.getMemoryFilePath(sessionId, key);
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const entry = JSON.parse(content) as MemoryEntry;
      return entry.value;
    } catch {
      return null;
    }
  }

  async compact(sessionId: string): Promise<void> {
    const sessionDir = this.getSessionDir(sessionId);
    try {
      const entries = await fs.readdir(sessionDir);
      const compacted: Record<string, unknown> = {};
      for (const file of entries) {
        const content = await fs.readFile(path.join(sessionDir, file), 'utf-8');
        const entry = JSON.parse(content) as MemoryEntry;
        compacted[entry.key] = entry.value;
      }

      const compactFile = path.join(this.storageDir, `${sessionId}-compacted.json`);
      await fs.writeFile(compactFile, JSON.stringify(compacted));

      for (const file of entries) {
        await fs.unlink(path.join(sessionDir, file));
      }
    } catch {
      // Session dir may not exist yet
    }
  }

  async list(sessionId: string): Promise<string[]> {
    const sessionDir = this.getSessionDir(sessionId);
    try {
      const entries = await fs.readdir(sessionDir);
      return entries.map(f => f.replace('.json', ''));
    } catch {
      return [];
    }
  }

  async clear(sessionId: string): Promise<void> {
    const sessionDir = this.getSessionDir(sessionId);
    await fs.rm(sessionDir, { recursive: true, force: true });
  }

  private async ensureStorageDir(): Promise<void> {
    await fs.mkdir(this.storageDir, { recursive: true });
  }

  private getSessionDir(sessionId: string): string {
    return path.join(this.storageDir, sessionId);
  }

  private getMemoryFilePath(sessionId: string, key: string): string {
    return path.join(this.getSessionDir(sessionId), `${key}.json`);
  }
}
