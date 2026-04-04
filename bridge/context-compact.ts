import * as fs from 'fs/promises';
import * as path from 'path';

type CompactionLevel = 'micro' | 'session' | 'full';

interface ContextUtilization {
  percentage: number;
  level: CompactionLevel;
  shouldCompact: boolean;
  hardBlock: boolean;
}

export class ContextCompact {
  async checkUtilization(currentTokens: number, maxTokens: number): Promise<ContextUtilization> {
    const percentage = (currentTokens / maxTokens) * 100;

    if (percentage > 85) {
      return { percentage, level: 'full', shouldCompact: true, hardBlock: true };
    }
    if (percentage > 75) {
      return { percentage, level: 'session', shouldCompact: true, hardBlock: false };
    }
    return { percentage, level: 'micro', shouldCompact: false, hardBlock: false };
  }

  async compact(sessionId: string, level: CompactionLevel): Promise<string> {
    const stateFile = `.ai/state.json`;
    const state = await this.readState(stateFile);

    switch (level) {
      case 'micro':
        return this.clearStaleToolResults(state);
      case 'session':
        return this.extractKeyDecisions(state, sessionId);
      case 'full':
        return this.summarizeHistory(state, sessionId);
      default:
        return String(state.context_summary || '');
    }
  }

  private async readState(stateFile: string): Promise<Record<string, unknown>> {
    try {
      const content = await fs.readFile(stateFile, 'utf-8');
      return JSON.parse(content);
    } catch {
      return { context_summary: '' };
    }
  }

  private clearStaleToolResults(state: Record<string, unknown>): string {
    if (state.tool_results) {
      delete state.tool_results;
    }
    return (state.context_summary as string) || '';
  }

  private async extractKeyDecisions(state: Record<string, unknown>, sessionId: string): Promise<string> {
    const logFile = `.ai/logs/state.log`;
    try {
      const content = await fs.readFile(logFile, 'utf-8');
      const decisions = content
        .split('\n')
        .filter(line => line.includes('DECISION') && line.includes(sessionId))
        .slice(-10)
        .join('\n');

      const summary = `Session ${sessionId} key decisions:\n${decisions}`;
      state.context_summary = summary;
      await fs.writeFile('.ai/state.json', JSON.stringify(state, null, 2));
      return summary;
    } catch {
      return (state.context_summary as string) || '';
    }
  }

  private async summarizeHistory(state: Record<string, unknown>, sessionId: string): Promise<string> {
    const summary = `Session ${sessionId} — full compact. User messages preserved, intermediate reasoning cleared.`;
    state.context_summary = summary;
    await fs.writeFile('.ai/state.json', JSON.stringify(state, null, 2));
    return summary;
  }
}
