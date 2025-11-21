// Simple proxy service for OpenRouteService - Node.js/Express version

// Come usare:
// 1. Installa le dipendenze con: npm install express node-fetch@2 cors
// 2. Inserisci la tua API key ORS qui sotto
// 3. Avvia con: node service.js
// (il frontend può chiamare POST http://localhost:3000/route)

const express = require('express');
const fetch = require('node-fetch'); // Usa v2 per la compatibilità require
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const ORS_API_KEY = '<INSERISCI_LA_TUA_API_KEY>'; // Sostituisci qui la tua chiave ORS!

app.post('/route', async (req, res) => {
  const { coordinates, mode } = req.body;
  const url = `https://api.openrouteservice.org/v2/directions/${mode}/geojson`;

  try {
    const orsRes = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ coordinates })
    });
    if (!orsRes.ok) {
      return res.status(orsRes.status).json({ error: 'OpenRouteService error', status: orsRes.status });
    }
    const data = await orsRes.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Proxy server error', details: err.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`ORS proxy service running on http://localhost:${PORT}/route`);
})