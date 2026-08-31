const CACHE_VERSION = 't7a-push-v3';

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', event => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (_) {
    try { data = { body: event.data ? event.data.text() : '' }; } catch (_) { data = {}; }
  }
  const title = data.title || 'Painel T7A';
  const options = {
    body: data.body || data.message || 'Você tem uma nova atualização.',
    icon: data.icon || '/apple-touch-icon.png',
    badge: data.badge || '/apple-touch-icon.png',
    data: { url: data.url || data.link || '/', ...((data.data && typeof data.data === 'object') ? data.data : {}) },
    tag: data.tag || undefined,
    renotify: Boolean(data.renotify),
    vibrate: [120, 60, 120]
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const targetUrl = event.notification?.data?.url || '/';
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const client of windows) {
      if ('focus' in client) {
        try { if ('navigate' in client) await client.navigate(targetUrl); } catch (_) {}
        return client.focus();
      }
    }
    if (self.clients.openWindow) return self.clients.openWindow(targetUrl);
  })());
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || !url.pathname.endsWith('/base-index.html')) return;

  event.respondWith((async () => {
    const response = await fetch(event.request);
    const contentType = response.headers.get('content-type') || '';
    if (!response.ok || !contentType.includes('text/html')) return response;

    let html = await response.text();
    if (!html.includes('id="sw-stable-menu-account-fix"')) {
      const css = `<style id="sw-stable-menu-account-fix">
@media(max-width:1023px){
#mobile-menu-stable .mms-sheet{max-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 104px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
#mobile-menu-stable .mms-account{margin-top:8px;padding-top:10px;border-top:1px solid rgba(148,163,184,.12)}
#mobile-menu-stable .mms-account-title{padding:0 6px 8px;font:800 9px/1 'Outfit',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#71717a}
#mobile-menu-stable .mms-account-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
#mobile-menu-stable .mms-account-btn{min-height:46px;border-radius:13px;border:1px solid rgba(148,163,184,.12);background:rgba(255,255,255,.035);color:#d4d4d8;font:750 12px/1.1 'Outfit',sans-serif;display:flex;align-items:center;justify-content:center;gap:7px;padding:8px 10px}
#mobile-menu-stable .mms-account-btn:active{transform:scale(.985)}
#mobile-menu-stable .mms-account-btn.admin{grid-column:1/-1;color:#a5b4fc;background:rgba(79,70,229,.12);border-color:rgba(99,102,241,.22)}
#mobile-menu-stable .mms-account-btn.logout{color:#fb7185;background:rgba(244,63,94,.08);border-color:rgba(244,63,94,.16)}
#mobile-menu-stable .mms-accent{display:flex;align-items:center;justify-content:center;gap:8px}
#mobile-menu-stable .mms-dot{width:18px;height:18px;border-radius:999px;border:2px solid rgba(255,255,255,.55);box-shadow:0 0 0 1px rgba(255,255,255,.08)}
#mobile-menu-stable .mms-dot.blue{background:#3b82f6}.mms-dot.pink{background:#ec4899}
html:not(.dark) #mobile-menu-stable .mms-account-btn{background:rgba(15,23,42,.035);color:#334155;border-color:rgba(15,23,42,.09)}
}
</style>`;
      const js = `<script id="sw-stable-menu-account-fix-script">
(()=>{
 const montar=()=>{
  if(innerWidth>=1024) return;
  const root=document.getElementById('mobile-menu-stable');
  const list=root?.querySelector('.mms-list');
  if(!root||!list||root.querySelector('.mms-account')) return;
  const box=document.createElement('div');
  box.className='mms-account';
  box.innerHTML='<div class="mms-account-title">Conta e aparência</div><div class="mms-account-grid"><button type="button" class="mms-account-btn mms-accent" data-a="blue"><span class="mms-dot blue"></span>Azul</button><button type="button" class="mms-account-btn mms-accent" data-a="pink"><span class="mms-dot pink"></span>Rosa</button><button type="button" class="mms-account-btn" data-a="theme">☀︎/☾ Tema</button><button type="button" class="mms-account-btn logout" data-a="logout">Sair</button><button type="button" class="mms-account-btn admin" data-a="admin">Painel Admin</button></div>';
  list.appendChild(box);
  box.addEventListener('click',e=>{
   const b=e.target.closest('[data-a]'); if(!b) return;
   const a=b.dataset.a;
   if(a==='blue'&&typeof window.alterarCorPainel==='function') window.alterarCorPainel('azul');
   else if(a==='pink'&&typeof window.alterarCorPainel==='function') window.alterarCorPainel('rosa');
   else if(a==='theme'&&typeof window.alternarTema==='function') window.alternarTema();
   else if(a==='logout'&&typeof window.sairSistema==='function') window.sairSistema();
   else if(a==='admin'&&typeof window.alternarModo==='function'){ root.classList.remove('is-open'); document.documentElement.style.overflow=''; window.alternarModo('admin'); }
  });
 };
 const tentar=()=>{montar(); if(!document.querySelector('#mobile-menu-stable .mms-account')) setTimeout(tentar,150)};
 if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',tentar,{once:true}); else tentar();
})();
</script>`;
      html = html.replace('</head>', `${css}</head>`).replace('</body>', `${js}</body>`);
    }

    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.set('cache-control', 'no-store');
    return new Response(html, { status: response.status, statusText: response.statusText, headers });
  })());
});
