export const VDS_THREADS_DEST = '/root/zynthio/_meta/threads/' as const;
export const MESH_HOST = '100.121.107.112' as const;
export const ORIGIN_HOST = '5.189.143.170' as const;
export const HEADSCALE = 'https://headscale.kamals.pro' as const;

export type CursorThread = {
  ok: true;
  kind: 'cursor_agent';
  id: string;
  title: string;
  url: string;
  status: 'RUNNING' | 'ERROR';
  branch: string | null;
  repo: 'coreintentdev/Zynthio';
};

export type GithubThread = {
  ok: true;
  kind: 'github_pr' | 'github_issue';
  id: string;
  title: string;
  url: string;
  status: 'open' | 'closed';
  draft?: boolean;
  repo: 'coreintentdev/Zynthio';
};

export type WorkspaceThread = CursorThread | GithubThread;

export type HandoverPack = {
  ok: true;
  dest: typeof VDS_THREADS_DEST;
  repo: 'coreintentdev/Zynthio';
  generated: '2026-10-08';
  pipe: { git: 'ops/_meta staged for VDS clone'; mesh: 'rsync when ssh_ok' };
  threads: WorkspaceThread[];
  facts: {
    jev: {
      role: 'Paid TypeSafe infrastructure';
      endpoint: 'https://api.typesafe.ai/v1/systemone';
      model: 'jev-latest';
      threshold: 0.85;
      method: 'POST';
      site: 'https://jevsdev.com is x-fleet-catchall HTML — not the API';
      inference: 'this repo does not POST (no spend)';
    };
    hermes: { lane: 'mesh-only'; port: 8000; note: 'left alone' };
    coreyai: {
      live_files: { present: false; path: '/var/www/html/coreyai.ai' };
      public: 'HTTP 403 from public internet';
      not_ours: 'coreyai.com parked Afternic/GoDaddy';
    };
    vds: {
      mesh: typeof MESH_HOST;
      origin: typeof ORIGIN_HOST;
      headscale: typeof HEADSCALE;
      ask_pr: 'https://github.com/coreintentdev/Zynthio/pull/12';
    };
  };
};

export const THREADS: WorkspaceThread[] = [
  {
    ok: true,
    kind: 'cursor_agent',
    id: 'bc-b5ce8a78-8bbf-575a-9267-d2cd88a498f5',
    title: 'Use credit: search CoreyAI in repo',
    url: 'https://cursor.com/agents/bc-b5ce8a78-8bbf-575a-9267-d2cd88a498f5',
    status: 'RUNNING',
    branch: 'cursor-ask-coreyai-98f5',
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'cursor_agent',
    id: 'bc-141b5c21-c6b6-5b6c-8efc-95df740150cd',
    title: 'Test CoreyAI ask form',
    url: 'https://cursor.com/agents/bc-141b5c21-c6b6-5b6c-8efc-95df740150cd',
    status: 'ERROR',
    branch: null,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '12',
    title: 'Typesafe ask for CoreyAI — JEV and Hermes lanes left alone',
    url: 'https://github.com/coreintentdev/Zynthio/pull/12',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '9',
    title: 'Real seven-brand ecosystem landing page for zynthio.ai',
    url: 'https://github.com/coreintentdev/Zynthio/pull/9',
    status: 'closed',
    draft: false,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '8',
    title: 'Sync all branches: merge music/pipeline-2026-05-12 into main',
    url: 'https://github.com/coreintentdev/Zynthio/pull/8',
    status: 'closed',
    draft: false,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '7',
    title: 'chore(music): bump pipeline docs to 2026-05-12; fix calendar table; add README section',
    url: 'https://github.com/coreintentdev/Zynthio/pull/7',
    status: 'closed',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '6',
    title: 'feat(music): DJ Zynrose music pipeline & DistroKid prep',
    url: 'https://github.com/coreintentdev/Zynthio/pull/6',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '5',
    title: 'feat(music): DJ Zynrose music pipeline & DistroKid prep scaffold',
    url: 'https://github.com/coreintentdev/Zynthio/pull/5',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '4',
    title: 'feat: DJ Zynrose music pipeline & DistroKid prep scaffolding',
    url: 'https://github.com/coreintentdev/Zynthio/pull/4',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '3',
    title: 'feat(music): DJ Zynrose music pipeline scaffold',
    url: 'https://github.com/coreintentdev/Zynthio/pull/3',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '2',
    title: 'feat: music pipeline scaffolding for DJ Zynrose / SongPal',
    url: 'https://github.com/coreintentdev/Zynthio/pull/2',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_pr',
    id: '1',
    title: 'Add music pipeline for DJ Zynrose / SongPal',
    url: 'https://github.com/coreintentdev/Zynthio/pull/1',
    status: 'open',
    draft: true,
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_issue',
    id: '11',
    title: 'Grok Build CLI Ongoing + Escalated Abuse - Emotional Framing + Stalling on Reversible Sovereign Work (2026-05-28)',
    url: 'https://github.com/coreintentdev/Zynthio/issues/11',
    status: 'open',
    repo: 'coreintentdev/Zynthio'
  },
  {
    ok: true,
    kind: 'github_issue',
    id: '10',
    title: 'Grok CLI Build Abuse Escalation - Happy Hard Core Mode Activated - 2026-05-28',
    url: 'https://github.com/coreintentdev/Zynthio/issues/10',
    status: 'open',
    repo: 'coreintentdev/Zynthio'
  }
];

export const PACK: HandoverPack = {
  ok: true,
  dest: VDS_THREADS_DEST,
  repo: 'coreintentdev/Zynthio',
  generated: '2026-10-08',
  pipe: { git: 'ops/_meta staged for VDS clone', mesh: 'rsync when ssh_ok' },
  threads: THREADS,
  facts: {
    jev: {
      role: 'Paid TypeSafe infrastructure',
      endpoint: 'https://api.typesafe.ai/v1/systemone',
      model: 'jev-latest',
      threshold: 0.85,
      method: 'POST',
      site: 'https://jevsdev.com is x-fleet-catchall HTML — not the API',
      inference: 'this repo does not POST (no spend)'
    },
    hermes: { lane: 'mesh-only', port: 8000, note: 'left alone' },
    coreyai: {
      live_files: { present: false, path: '/var/www/html/coreyai.ai' },
      public: 'HTTP 403 from public internet',
      not_ours: 'coreyai.com parked Afternic/GoDaddy'
    },
    vds: {
      mesh: MESH_HOST,
      origin: ORIGIN_HOST,
      headscale: HEADSCALE,
      ask_pr: 'https://github.com/coreintentdev/Zynthio/pull/12'
    }
  }
};

export type SecretShape = 'missing' | 'placeholder' | 'present';

export function sshKeyShape(value: string | undefined): SecretShape {
  if (!value) return 'missing';
  if (value.includes('BEGIN') && value.length >= 200) return 'present';
  return 'placeholder';
}

export function preauthShape(value: string | undefined): SecretShape {
  if (!value) return 'missing';
  if (value.length >= 24) return 'present';
  return 'placeholder';
}

export type PushReady = { ok: true; dest: typeof VDS_THREADS_DEST; host: typeof MESH_HOST };

export type PushBlocked = {
  ok: false;
  dest: typeof VDS_THREADS_DEST;
  error: 'ssh_key_placeholder' | 'mesh_key_placeholder' | 'mesh_unreachable' | 'ssh_fail';
  ssh_key: SecretShape;
  mesh_key: SecretShape;
  mesh_ping: boolean;
  landed: false;
};

export type PushResult = PushReady | PushBlocked;

export function inspectPush(input: {
  sshKey?: string;
  preauth?: string;
  meshPing: boolean;
}): PushResult {
  const ssh_key = sshKeyShape(input.sshKey);
  const mesh_key = preauthShape(input.preauth);
  if (ssh_key !== 'present') {
    return {
      ok: false,
      dest: VDS_THREADS_DEST,
      error: 'ssh_key_placeholder',
      ssh_key,
      mesh_key,
      mesh_ping: input.meshPing,
      landed: false
    };
  }
  if (mesh_key !== 'present') {
    return {
      ok: false,
      dest: VDS_THREADS_DEST,
      error: 'mesh_key_placeholder',
      ssh_key,
      mesh_key,
      mesh_ping: input.meshPing,
      landed: false
    };
  }
  if (!input.meshPing) {
    return {
      ok: false,
      dest: VDS_THREADS_DEST,
      error: 'mesh_unreachable',
      ssh_key,
      mesh_key,
      mesh_ping: false,
      landed: false
    };
  }
  return { ok: true, dest: VDS_THREADS_DEST, host: MESH_HOST };
}
