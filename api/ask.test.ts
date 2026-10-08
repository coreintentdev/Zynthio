import assert from 'node:assert/strict';
import { test } from 'node:test';
import { answer } from './ask.ts';

test('what is on coreyai.ai is a typed hit with missing live tree', () => {
  const result = answer('what is on coreyai.ai');
  assert.equal(result.status, 200);
  assert.equal(result.body.ok, true);
  if (result.body.ok !== true) throw new Error('expected hit');
  assert.equal(result.body.kind, 'site');
  assert.equal(result.body.name, 'CoreeyAI');
  assert.equal(result.body.source, 'public/index.html');
  if (result.body.kind !== 'site') throw new Error('expected site');
  assert.equal(result.body.live_files?.present, false);
  assert.equal(result.body.live_files?.path, '/var/www/html/coreyai.ai');
  assert.equal(result.body.urls.includes('https://coreyai.com'), false);
});

test('coreyai.com is typed not-ours', () => {
  const result = answer('coreyai.com');
  assert.equal(result.status, 404);
  assert.equal(result.body.ok, false);
  if (result.body.ok !== false) throw new Error('expected miss');
  assert.equal(result.body.error, 'not ours');
});

test('JEV is TypeSafe API, not the jevsdev.com catchall site', () => {
  const result = answer('what is jev');
  assert.equal(result.status, 200);
  assert.equal(result.body.ok, true);
  if (result.body.ok !== true) throw new Error('expected hit');
  assert.equal(result.body.kind, 'jev');
  if (result.body.kind !== 'jev') throw new Error('expected jev');
  assert.equal(result.body.endpoint, 'https://api.typesafe.ai/v1/systemone');
  assert.equal(result.body.model, 'jev-latest');
  assert.equal(result.body.threshold, 0.85);
  assert.equal(result.body.method, 'POST');
  assert.equal(result.body.site.url, 'https://jevsdev.com');
  const siteQ = answer('what is on jevsdev.com');
  assert.equal(siteQ.status, 200);
  if (siteQ.body.ok !== true || siteQ.body.kind !== 'jev') throw new Error('expected jev');
  assert.match(siteQ.body.site.note, /catchall/);
});

test('empty question is typed 400', () => {
  const result = answer('');
  assert.equal(result.status, 400);
  assert.equal(result.body.ok, false);
  if (result.body.ok !== false) throw new Error('expected miss');
  assert.equal(result.body.error, 'question required');
});
