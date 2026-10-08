import { spawnSync } from 'node:child_process';
import { inspectPush, MESH_HOST, PACK, VDS_THREADS_DEST, type PushResult } from './threads.ts';

function pingMesh(): boolean {
  const result = spawnSync('ping', ['-c', '1', '-W', '2', MESH_HOST], { stdio: 'ignore' });
  return result.status === 0;
}

export function planPush(env: NodeJS.ProcessEnv = process.env): PushResult {
  return inspectPush({
    sshKey: env.ZYNTHIO_DC_SSH_KEY,
    preauth: env.HEADSCALE_PREAUTH_KEY,
    meshPing: pingMesh()
  });
}

export function main(): PushResult {
  const plan = planPush();
  process.stdout.write(`${JSON.stringify({ pack: PACK.ok, threads: PACK.threads.length, dest: VDS_THREADS_DEST, push: plan })}\n`);
  return plan;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const plan = main();
  process.exit(plan.ok ? 0 : 2);
}
