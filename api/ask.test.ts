import assert from 'node:assert/strict';
import { test } from 'node:test';
import { answer } from './ask.ts';

test('what is on coreyai.ai is a typed hit with missing live tree', () => {
  const result = answer('what is on coreyai.ai');
  assert.equal(result.status, 200);
  assert.equal(result.body.ok, true);
  if (result.body.ok !== true) throw new Error('expected hit');
  assert.equal(result.body.name, 'CoreeyAI');
  assert.equal(result.body.source, 'public/index.html');
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

test('jevsdev.com stays on the JEV lane', () => {
  const result = answer('what is on jevsdev.com');
  assert.equal(result.status, 404);
  assert.equal(result.body.ok, false);
  if (result.body.ok !== false) throw new Error('expected miss');
  assert.equal(result.body.error, 'not in this repo');
  if (result.body.error === 'not in this repo') {
    assert.equal(result.body.host, 'jevsdev.com');
    assert.match(result.body.missing ?? '', /JEV/);
  }
});

test('empty question is typed 400', () => {
  const result = answer('');
  assert.equal(result.status, 400);
  assert.equal(result.body.ok, false);
  if (result.body.ok !== false) throw new Error('expected miss');
  assert.equal(result.body.error, 'question required');
});
