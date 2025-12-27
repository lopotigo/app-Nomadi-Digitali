// public/js/init.js
(async function(){
  // safe fetch of /config
  async function getConfig() {
    try {
      const r = await fetch('/config', { cache: 'no-store' });
      if (!r.ok) throw new Error('config fetch failed: ' + r.status);
      return r.json();
    } catch (err) {
      console.error('[init] failed to load /config', err);
      return null;
    }
  }

  const cfg = await getConfig();
  if (!cfg || !cfg.SUPABASE_URL || !cfg.SUPABASE_ANON_KEY) {
    console.warn('[init] supabase config missing; client not created');
    return;
  }

  if (typeof createClient !== 'function') {
    console.error('[init] supabase createClient() not found. Ensure CDN script is loaded before this script.');
    return;
  }

  // create client and expose it for debug/consumption
  const supabase = createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);
  window.supabaseClient = supabase;          // stable global for debug
  window.supabase = supabase;                // alias (legacy)

  // Helper: structured error logging (stringified)
  function logSupabaseError(err, label = '') {
    try {
      console.error(`[supabase][${label}]`, JSON.stringify(err, Object.getOwnPropertyNames(err), 2));
    } catch (e) {
      console.error(`[supabase][${label}] (raw)`, err);
    }
  }

  // client-side wrapper for safe insert to smn_profiles_v1 (development)
  // Note: prefer server-side endpoint for production (below we'll add server route).
  async function insertProfileClient(payload = {}) {
    // minimal validation: check it's an object
    if (!payload || typeof payload !== 'object') {
      throw new Error('payload must be an object');
    }

    try {
      const { data, error } = await supabase.from('smn_profiles_v1').insert([payload]);
      if (error) {
        logSupabaseError(error, 'insertProfileClient');
        return { ok: false, error };
      }
      return { ok: true, data };
    } catch (e) {
      console.error('[insertProfileClient] unexpected', e);
      return { ok: false, error: e };
    }
  }

  // Expose a small API for the app to call
  window.appApi = window.appApi || {};
  window.appApi.supabaseClient = supabase;
  window.appApi.insertProfileClient = insertProfileClient;
  window.appApi._logError = logSupabaseError;

  console.info('[init] supabase client ready: window.supabaseClient and window.appApi.insertProfileClient available');
})();