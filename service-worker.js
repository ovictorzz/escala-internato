const CACHE_VERSION = 't7a-push-v4';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));

self.addEventListener('push', event => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; }
  catch (_) { try { data = { body: event.data ? event.data.text() : '' }; } catch (_) {} }
  event.waitUntil(self.registration.showNotification(data.title || 'Painel T7A', {
    body: data.body || data.message || 'Você tem uma nova atualização.',
    icon: data.icon || '/apple-touch-icon.png', badge: data.badge || '/apple-touch-icon.png',
    data: { url: data.url || data.link || '/', ...((data.data && typeof data.data === 'object') ? data.data : {}) },
    tag: data.tag || undefined, renotify: Boolean(data.renotify), vibrate: [120,60,120]
  }));
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const targetUrl = event.notification?.data?.url || '/';
  event.waitUntil((async()=>{
    const windows = await self.clients.matchAll({type:'window',includeUncontrolled:true});
    for (const client of windows) { try { if ('navigate' in client) await client.navigate(targetUrl); } catch (_) {} if ('focus' in client) return client.focus(); }
    if (self.clients.openWindow) return self.clients.openWindow(targetUrl);
  })());
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || !url.pathname.endsWith('/base-index.html')) return;
  event.respondWith((async()=>{
    const response = await fetch(event.request, {cache:'no-store'});
    const type = response.headers.get('content-type') || '';
    if (!response.ok || !type.includes('text/html')) return response;
    let html = await response.text();
    const css = `<style id="mobile-account-controls-v4">
@media(max-width:1023px){
#mobile-menu-stable .mms-sheet{max-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 100px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
#mobile-menu-stable .mms-account-v4{margin-top:8px;padding:11px 2px 2px;border-top:1px solid rgba(148,163,184,.13)}
#mobile-menu-stable .mms-account-v4-title{padding:0 7px 9px;font:800 9px/1 'Outfit',sans-serif;letter-spacing:.15em;text-transform:uppercase;color:#71717a}
#mobile-menu-stable .mms-account-v4-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
#mobile-menu-stable .mms-account-v4 button{min-height:47px;border-radius:13px;border:1px solid rgba(148,163,184,.13);background:rgba(255,255,255,.04);color:#e4e4e7;font:750 12px/1.1 'Outfit',sans-serif;padding:8px}
#mobile-menu-stable .mms-account-v4 .full{grid-column:1/-1}
#mobile-menu-stable .mms-account-v4 .admin{color:#a5b4fc;background:rgba(79,70,229,.12);border-color:rgba(99,102,241,.24)}
#mobile-menu-stable .mms-account-v4 .logout{color:#fb7185;background:rgba(244,63,94,.08)}
html:not(.dark) #mobile-menu-stable .mms-account-v4 button{color:#334155;background:rgba(15,23,42,.035)}
}
</style>`;
    const js = `<script id="mobile-account-controls-v4-script">
(()=>{
 const mount=()=>{
  if(innerWidth>=1024)return;
  const root=document.getElementById('mobile-menu-stable');
  const list=root?.querySelector('.mms-list');
  if(!root||!list||root.querySelector('.mms-account-v4'))return;
  const el=document.createElement('div'); el.className='mms-account-v4';
  el.innerHTML='<div class="mms-account-v4-title">Conta e aparência</div><div class="mms-account-v4-grid"><button data-x="blue">● Azul</button><button data-x="pink">● Rosa</button><button data-x="theme">☀︎ / ☾ Tema</button><button data-x="logout" class="logout">Sair</button><button data-x="admin" class="admin full">Painel Admin</button></div>';
  list.appendChild(el);
  el.onclick=e=>{const b=e.target.closest('button[data-x]');if(!b)return;const x=b.dataset.x;
   if(x==='blue') window.alterarCorPainel?.('azul');
   if(x==='pink') window.alterarCorPainel?.('rosa');
   if(x==='theme') window.alternarTema?.();
   if(x==='logout') window.sairSistema?.();
   if(x==='admin'){root.classList.remove('is-open');document.documentElement.style.overflow='';window.alternarModo?.('admin');}
  };
 };
 const loop=()=>{mount(); if(!document.querySelector('#mobile-menu-stable .mms-account-v4')) setTimeout(loop,100)};
 if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',loop,{once:true}); else loop();
 new MutationObserver(mount).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>`;
    if(!html.includes('mobile-account-controls-v4')) html=html.replace('</head>',css+'</head>').replace('</body>',js+'</body>');
    const headers=new Headers(response.headers);headers.delete('content-length');headers.set('cache-control','no-store, max-age=0');
    return new Response(html,{status:response.status,statusText:response.statusText,headers});
  })());
});
