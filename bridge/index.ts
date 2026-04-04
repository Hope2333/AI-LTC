/**
 * AI-LTC Bridge — Entry Point
 *
 * Thin adapter bridge between AI-LTC (Brain) and OML (Body).
 * Exports the OmlBridge class for state→hook mapping, memory routing,
 * capability discovery, and error handling.
 *
 * Design constraint: ~500 lines total across all bridge TypeScript files.
 */

export { OmlBridge } from './oml-bridge';
export { CapabilityRegistry } from './capability-registry';
export type { Capability, CapabilityResult } from './capability-registry';
