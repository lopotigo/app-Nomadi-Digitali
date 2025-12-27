````markdown
# Minimal Project (scaffold)

How to run locally:

1. Copy `.env.example` to `.env` and fill variables:
   cp .env.example .env
   # edit .env and set SUPABASE_URL and SUPABASE_ANON_KEY

2. Install dependencies:
   npm install

3. Start server:
   npm start

The server serves `public/universal-html.html` and exposes `/config` which returns SUPABASE_URL and SUPABASE_ANON_KEY to the browser (so you don't hardcode keys in HTML).

Note: Do NOT commit `.env` to version control. If you accidentally commit secrets, rotate them immediately.