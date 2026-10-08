const ORIGIN = 'https://zynthio.ai' as const;

export type AskSite = {
  ok: true;
  kind: 'site';
  name: string;
  role: string;
  description: string;
  urls: string[];
  source: 'public/index.html';
  live_files?: { present: false; path: string };
  public?: { url: string; note: string };
  not_ours?: { host: string; note: string }[];
};

export type AskJev = {
  ok: true;
  kind: 'jev';
  name: 'JEV';
  role: 'Paid TypeSafe infrastructure';
  description: string;
  urls: string[];
  source: 'https://api.typesafe.ai/health';
  endpoint: 'https://api.typesafe.ai/v1/systemone';
  model: 'jev-latest';
  threshold: 0.85;
  method: 'POST';
  site: { url: 'https://jevsdev.com'; note: 'x-fleet-catchall HTML — not the API' };
};

export type AskHit = AskSite | AskJev;

export type AskMiss = {
  ok: false;
  error: 'not in this repo';
  host?: string;
  missing?: string;
};

export type AskNotOurs = {
  ok: false;
  error: 'not ours';
  host: string;
  note: string;
};

export type AskBadRequest = { ok: false; error: 'question required' };
export type AskMethod = { ok: false; error: 'Method not allowed' };

export type AskBody = AskHit | AskMiss | AskNotOurs | AskBadRequest | AskMethod;

export type AskResult =
  | { status: 200; body: AskHit }
  | { status: 400; body: AskBadRequest }
  | { status: 404; body: AskMiss | AskNotOurs }
  | { status: 405; body: AskMethod };

type Site = {
  keys: string[];
  name: string;
  role: string;
  description: string;
  urls: string[];
  source: 'public/index.html';
  live_files?: { present: false; path: string };
  public?: { url: string; note: string };
  not_ours?: { host: string; note: string }[];
};

const SITES: Site[] = [
  {
    keys: ['zynthio.ai', 'zynthio.com', 'zynthio'],
    name: 'ZYNTHIO',
    role: 'Parent entity & sovereign infrastructure',
    description: 'The umbrella. Glass-box AI trading platform, sovereign matrix architecture, and the ecosystem operational backbone. ZYNTHIO LIMITED name reservation #15436626.',
    urls: ['https://zynthio.ai', 'https://zynthio.com'],
    source: 'public/index.html'
  },
  {
    keys: ['coreyai.ai', 'coreyai', 'coreeyai', 'corey ai', 'coreintentai'],
    name: 'CoreeyAI',
    role: 'AI intelligence layer',
    description: 'Multi-model orchestration engine. Claude, Grok, Perplexity routed through a hexagonal adapter layer with deterministic rule engines (PHREAK algorithm). The brain behind the trading decisions.',
    urls: ['https://coreyai.ai'],
    source: 'public/index.html',
    live_files: { present: false, path: '/var/www/html/coreyai.ai' },
    public: { url: 'https://coreyai.ai', note: 'HTTP 403 from the public internet' },
    not_ours: [{ host: 'coreyai.com', note: 'parked Afternic/GoDaddy — not owned' }]
  },
  {
    keys: ['songpal.ai', 'songpal'],
    name: 'SongPal',
    role: 'Audio platform & music distribution',
    description: 'Music creation, distribution, and the music-as-backup doctrine. 40+ tracks across 9+ languages with te reo Maori pillars. DistroKid distribution. IPONZ trademark #1318588 filed.',
    urls: ['https://songpal.ai'],
    source: 'public/index.html'
  },
  {
    keys: ['mosoko.ai', 'mosoko.io', 'mosoko'],
    name: 'MOSOKO',
    role: 'Fashion & creative design',
    description: 'Streetwear and creative fashion brand. Cultural fusion design with Aotearoa roots. Currently in design/concept phase with curriculum and product line in development.',
    urls: ['https://mosoko.ai'],
    source: 'public/index.html'
  },
  {
    keys: ['kervalon.ai', 'kervalon'],
    name: 'KERVALON',
    role: 'Education & research',
    description: 'Educational technology and research platform. Curriculum development, AI-assisted learning, and knowledge architecture. Building the next generation of creative-tech education.',
    urls: ['https://kervalon.ai'],
    source: 'public/index.html'
  },
  {
    keys: ['coreintent.dev', 'coreintent'],
    name: 'COREINTENT',
    role: 'Trading engine & developer tools',
    description: 'The core trading engine. Next.js 15, AI fleet, Commander Terminal. Agentic crypto trading with glass-box transparency. gTrade integration live. Open source.',
    urls: ['https://coreintent.dev'],
    source: 'public/index.html'
  },
  {
    keys: ['dj zynrose', 'zynrose'],
    name: 'DJ Zynrose',
    role: 'Artist alias & music production',
    description: 'Corey McIvor artist alias. Music production across genres: DnB, phonk, lo-fi, orchestral pop. 336 Hz subharmonic drone as catalog signature. Incident-tracks encode doctrine in lyric form.',
    urls: [],
    source: 'public/index.html'
  }
];

const NOT_IN_THIS_REPO: Record<string, AskMiss | AskNotOurs> = {
  'coreyai.com': {
    ok: false,
    error: 'not ours',
    host: 'coreyai.com',
    note: 'parked Afternic/GoDaddy — not owned'
  },
  'zyncontext.ai': {
    ok: false,
    error: 'not in this repo',
    host: 'zyncontext.ai',
    missing: '/root/sites/zyncontext'
  },
  'sublimeoracle.com': {
    ok: false,
    error: 'not in this repo',
    host: 'sublimeoracle.com',
    missing: 'not in this repo'
  },
  'agentictwin.dev': {
    ok: false,
    error: 'not in this repo',
    host: 'agentictwin.dev',
    missing: 'not in this repo'
  },
};

function payload(site: Site): AskSite {
  const body: AskSite = {
    ok: true,
    kind: 'site',
    name: site.name,
    role: site.role,
    description: site.description,
    urls: site.urls,
    source: site.source
  };
  if (site.live_files) body.live_files = site.live_files;
  if (site.public) body.public = site.public;
  if (site.not_ours) body.not_ours = site.not_ours;
  return body;
}

const JEV: AskJev = {
  ok: true,
  kind: 'jev',
  name: 'JEV',
  role: 'Paid TypeSafe infrastructure',
  description: 'POST https://api.typesafe.ai/v1/systemone with model jev-latest and a 0.85 gate. GET /health is the API. jevsdev.com is a fleet catchall website, not JEV.',
  urls: ['https://api.typesafe.ai/v1/systemone', 'https://api.typesafe.ai/health'],
  source: 'https://api.typesafe.ai/health',
  endpoint: 'https://api.typesafe.ai/v1/systemone',
  model: 'jev-latest',
  threshold: 0.85,
  method: 'POST',
  site: { url: 'https://jevsdev.com', note: 'x-fleet-catchall HTML — not the API' }
};

function escapeRegex(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function matchesKey(query: string, key: string): boolean {
  return new RegExp(`(^|[^a-z0-9])${escapeRegex(key)}([^a-z0-9]|$)`).test(query);
}

function isJevQuestion(q: string): boolean {
  return (
    q.includes('typesafe.ai') ||
    q.includes('jev-latest') ||
    q.includes('jevsdev') ||
    /(^|[^a-z])jev([^a-z]|$)/.test(q)
  );
}

export function answer(question: unknown): AskResult {
  const q = String(question ?? '').toLowerCase();
  if (!q.trim()) return { status: 400, body: { ok: false, error: 'question required' } };

  if (isJevQuestion(q)) return { status: 200, body: JEV };

  for (const host of Object.keys(NOT_IN_THIS_REPO)) {
    if (!q.includes(host)) continue;
    if (host === 'coreyai.com' && q.includes('coreyai.ai')) continue;
    const body = NOT_IN_THIS_REPO[host];
    if (!body) continue;
    return { status: 404, body };
  }

  const site = SITES.find((s) => s.keys.some((key) => matchesKey(q, key)));
  if (!site) return { status: 404, body: { ok: false, error: 'not in this repo' } };
  return { status: 200, body: payload(site) };
}

type VercelReq = {
  method?: string;
  query?: { q?: string | string[] };
  body?: { q?: unknown };
};

type VercelRes = {
  setHeader: (name: string, value: string) => void;
  status: (code: number) => VercelRes;
  json: (body: AskBody) => unknown;
  end: () => unknown;
};

export default async function handler(req: VercelReq, res: VercelRes): Promise<unknown> {
  res.setHeader('Access-Control-Allow-Origin', ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }
  const raw = req.method === 'GET' ? req.query?.q : req.body?.q;
  const question = Array.isArray(raw) ? raw[0] : raw;
  const result = answer(question);
  return res.status(result.status).json(result.body);
}
