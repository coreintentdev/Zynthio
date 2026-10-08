import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { inspectPush, PACK, THREADS, VDS_THREADS_DEST, preauthShape, sshKeyShape } from './threads.ts';

const root = join(dirname(fileURLToPath(import.meta.url)), '../..');

test('workspace pack lists both Cursor threads and GitHub PRs/issues', () => {
  assert.equal(PACK.ok, true);
  assert.equal(PACK.dest, VDS_THREADS_DEST);
  assert.equal(PACK.facts.jev.endpoint, 'https://api.typesafe.ai/v1/systemone');
  assert.equal(PACK.facts.jev.model, 'jev-latest');
  assert.equal(PACK.facts.hermes.port, 8000);
  assert.equal(PACK.facts.coreyai.live_files.path, '/var/www/html/coreyai.ai');
  const agents = THREADS.filter((t) => t.kind === 'cursor_agent');
  assert.equal(agents.length, 2);
  assert.ok(THREADS.some((t) => t.kind === 'github_pr' && t.id === '12'));
  assert.ok(THREADS.some((t) => t.kind === 'github_issue' && t.id === '11'));
});

test('committed JSON pack matches typed THREADS', () => {
  const jsonPath = join(root, '_meta/threads/zynthio-workspace-2026-10-08.json');
  const onDisk = JSON.parse(readFileSync(jsonPath, 'utf8')) as typeof PACK;
  assert.deepEqual(onDisk.threads, THREADS);
  assert.equal(onDisk.dest, '/root/zynthio/_meta/threads/');
  assert.equal(onDisk.facts.jev.endpoint, PACK.facts.jev.endpoint);
});

test('placeholder secrets block VDS rsync — do not claim landed', () => {
  const blocked = inspectPush({ sshKey: 'placeholder', preauth: 'placeholder', meshPing: false });
  assert.equal(blocked.ok, false);
  if (blocked.ok) throw new Error('expected block');
  assert.equal(blocked.error, 'ssh_key_placeholder');
  assert.equal(blocked.landed, false);
  assert.equal(sshKeyShape('short'), 'placeholder');
  assert.equal(preauthShape('x'.repeat(12)), 'placeholder');
});

test('real-shaped keys with mesh down still do not land', () => {
  const pem = `-----BEGIN OPENSSH PRIVATE KEY-----\n${'A'.repeat(200)}\n-----END OPENSSH PRIVATE KEY-----`;
  const blocked = inspectPush({ sshKey: pem, preauth: 'hs_preauth_key_value_long_enough', meshPing: false });
  assert.equal(blocked.ok, false);
  if (blocked.ok) throw new Error('expected block');
  assert.equal(blocked.error, 'mesh_unreachable');
  assert.equal(blocked.landed, false);
});

test('real-shaped keys and mesh ping are ready for rsync', () => {
  const pem = `-----BEGIN OPENSSH PRIVATE KEY-----\n${'A'.repeat(200)}\n-----END OPENSSH PRIVATE KEY-----`;
  const ready = inspectPush({ sshKey: pem, preauth: 'hs_preauth_key_value_long_enough', meshPing: true });
  assert.equal(ready.ok, true);
  if (!ready.ok) throw new Error('expected ready');
  assert.equal(ready.dest, VDS_THREADS_DEST);
  assert.equal(ready.host, '100.121.107.112');
});
