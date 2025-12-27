// server/index.js
// Simple Express server that serves `public/` and returns client-safe config at /config
require('dotenv').config();
const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files in public/
const publicDir = path.join(__dirname, '..', 'public');
app.use(express.static(publicDir));

// Endpoint that returns public config for client (only values you choose to expose)
app.get('/config', (req, res) => {
  const cfg = {
    SUPABASE_URL: process.env.SUPABASE_URL || '',
    SUPABASE_ANON_KEY: process.env.SUPABASE_ANON_KEY || ''
  };
  res.json(cfg);
});

// Fallback to index if using client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(publicDir, 'universal-html.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});