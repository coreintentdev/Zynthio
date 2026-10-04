const ORIGIN = 'https://zynthio.ai';

// Brand cards already in public/index.html. Not the live VDS trees.
const SITES = [
  {
    keys: ['zynthio.ai', 'zynthio.com', 'zynthio'],
    name: 'ZYNTHIO',
    role: 'Parent entity & sovereign infrastructure',
    description: 'The umbrella. Glass-box AI trading platform, sovereign matrix architecture, and the ecosystem operational backbone. ZYNTHIO LIMITED name reservation #15436626.',
    urls: ['https://zynthio.ai', 'https://zynthio.com'],
    source: 'public/index.html'
  },
  {
    keys: ['coreyai.ai', 'coreyai', 'coreeyai', 'corey ai'],
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

const NOT_IN_THIS_REPO = {
  'coreyai.com': {
    error: 'not ours',
    host: 'coreyai.com',
    note: 'parked Afternic/GoDaddy — not owned'
  },
  'zyncontext.ai': {
    error: 'not in this repo',
    host: 'zyncontext.ai',
    missing: '/root/sites/zyncontext'
  },
  'sublimeoracle.com': {
    error: 'not in this repo',
    host: 'sublimeoracle.com',
    missing: 'not in this repo'
  },
  'agentictwin.dev': {
    error: 'not in this repo',
    host: 'agentictwin.dev',
    missing: 'not in this repo'
  }
};

function payload(site) {
  const body = {
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

export function answer(question) {
  const q = String(question || '').toLowerCase();
  if (!q.trim()) return { status: 400, body: { error: 'question required' } };

  for (const host of Object.keys(NOT_IN_THIS_REPO)) {
    if (!q.includes(host)) continue;
    if (host === 'coreyai.com' && q.includes('coreyai.ai')) continue;
    return { status: 404, body: NOT_IN_THIS_REPO[host] };
  }

  const site = SITES.find((s) => s.keys.some((key) => q.includes(key)));
  if (!site) return { status: 404, body: { error: 'not in this repo' } };
  return { status: 200, body: payload(site) };
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const question = req.method === 'GET' ? req.query?.q : req.body?.q;
  const result = answer(question);
  return res.status(result.status).json(result.body);
}
