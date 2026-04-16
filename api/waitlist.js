export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyP_D_HNS-UK2BnQtsYTL-zTUPHCY40rIhVLZFVpEW9s39pqAXqteBZAExh6Y5fIpfhTg/exec';

  try {
    await fetch(GOOGLE_SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    });

    res.setHeader('Access-Control-Allow-Origin', '*');
    return res.status(200).json({ status: 'ok' });
  } catch (err) {
    return res.status(500).json({ error: 'Failed to submit' });
  }
}
