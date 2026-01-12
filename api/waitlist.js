const RESEND_API_KEY = process.env.RESEND_API_KEY;
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const { email } = req.body;
  if (!email || !email.includes('@')) return res.status(400).json({ error: 'Valid email required' });
  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Zynthio <onboarding@resend.dev>',
        to: [email],
        subject: 'Welcome to Zynthio Waitlist',
        html: `<div style="font-family:monospace;background:#0a0a0a;color:#e0e0e0;padding:40px;text-align:center"><h1 style="color:#00ff9d;text-transform:uppercase;letter-spacing:4px">ZYNTHIO</h1><p style="font-size:18px">You're on the list.</p><p>Launch: <strong>January 17, 2026</strong></p><p style="margin-top:30px;color:#888">MAXIMIZING ALPHA. MINIMIZING TRUST.</p><a href="https://github.com/coreintentdev/coreintentai" style="display:inline-block;margin-top:20px;border:1px solid #00ff9d;color:#00ff9d;padding:12px 24px;text-decoration:none">VIEW SOURCE</a></div>`
      })
    });
    if (!response.ok) throw new Error('Failed to send email');
    return res.status(200).json({ success: true });
  } catch (error) {
    return res.status(500).json({ error: 'Failed to process request' });
  }
}
