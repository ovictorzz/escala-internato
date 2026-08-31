const CACHE_VERSION = 't7a-push-v7';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));

self.addEventListener('push', event => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; }
  catch (_) { try { data = { body: event.data ? event.data.text() : '' }; } catch (_) {} }
  event.waitUntil(self.registration.showNotification(data.title || 'Painel T7A', {
    body: data.body || data.message || 'Você tem uma nova atualização.',
    icon: data.icon || '/apple-touch-icon.png',
    badge: data.badge || '/apple-touch-icon.png',
    data: { url: data.url || data.link || '/', ...((data.data && typeof data.data === 'object') ? data.data : {}) },
    tag: data.tag || undefined,
    renotify: Boolean(data.renotify),
    vibrate: [120,60,120]
  }));
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const targetUrl = event.notification?.data?.url || '/';
  event.waitUntil((async()=>{
    const windows = await self.clients.matchAll({type:'window', includeUncontrolled:true});
    for (const client of windows) {
      try { if ('navigate' in client) await client.navigate(targetUrl); } catch (_) {}
      if ('focus' in client) return client.focus();
    }
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

    const css = `<style id="mobile-account-controls-v7">
@media(max-width:1023px){
#mobile-menu-stable .mms-sheet{max-height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom) - 100px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
#mobile-menu-stable .mms-account-v7{display:block!important;visibility:visible!important;opacity:1!important;margin-top:8px;padding:11px 2px 2px;border-top:1px solid rgba(148,163,184,.13)}
#mobile-menu-stable .mms-account-v7-title{padding:0 7px 9px;font:800 9px/1 'Outfit',sans-serif;letter-spacing:.15em;text-transform:uppercase;color:#71717a}
#mobile-menu-stable .mms-account-v7-grid{display:grid!important;grid-template-columns:1fr 1fr;gap:7px}
#mobile-menu-stable .mms-account-v7 button{display:flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;min-height:47px;border-radius:13px;border:1px solid rgba(148,163,184,.13);background:rgba(255,255,255,.04);color:#e4e4e7;font:750 12px/1.1 'Outfit',sans-serif;padding:8px}
#mobile-menu-stable .mms-account-v7 .full{grid-column:1/-1}
#mobile-menu-stable .mms-account-v7 .admin{color:#a5b4fc;background:rgba(79,70,229,.12);border-color:rgba(99,102,241,.24)}
#mobile-menu-stable .mms-account-v7 .logout{color:#fb7185;background:rgba(244,63,94,.08);border-color:rgba(244,63,94,.18)}
#mobile-menu-stable .mms-swatch{width:20px;height:20px;border-radius:999px;display:inline-block;flex:0 0 20px;border:2px solid rgba(255,255,255,.72);box-shadow:0 0 0 1px rgba(255,255,255,.08),0 3px 10px rgba(0,0,0,.28)}
#mobile-menu-stable .mms-swatch.blue{background:#3b82f6}
#mobile-menu-stable .mms-swatch.pink{background:#ec4899}
html:not(.dark) #mobile-menu-stable .mms-account-v7 button{color:#334155;background:rgba(15,23,42,.035)}
html:not(.dark) #mobile-menu-stable .mms-swatch{border-color:rgba(255,255,255,.95);box-shadow:0 0 0 1px rgba(15,23,42,.12),0 3px 10px rgba(15,23,42,.12)}
}
</style>`;

    const js = `<script id="mobile-account-controls-v7-script">
(()=>{
 const irParaLogin=()=>{
  try {
   sessionStorage.removeItem('autenticado');
   sessionStorage.removeItem('alunoLogado');
   sessionStorage.removeItem('adminAutenticado');
  } catch (_) {}
  const menu=document.getElementById('mobile-menu-stable');
  if(menu) menu.classList.remove('is-open');
  document.documentElement.style.overflow='';
  document.body.classList.remove('app-authenticated');
  const login=document.getElementById('login-overlay');
  if(login){
   login.style.display='flex';
   login.classList.remove('hidden');
   login.style.visibility='visible';
   login.style.opacity='1';
  } else {
   location.replace('/');
  }
 };

 const mount=()=>{
  if(innerWidth>=1024) return;
  const root=document.getElementById('mobile-menu-stable');
  const list=root?.querySelector('.mms-list');
  if(!root||!list) return;

  root.querySelectorAll('.mms-account-v4,.mms-account-v5,.mms-account-v6,.mms-account-v7').forEach(node=>{ if(!node.classList.contains('mms-account-v7')) node.remove(); });
  let el=root.querySelector('.mms-account-v7');
  if(!el){
   el=document.createElement('div');
   el.className='mms-account-v7';
   el.innerHTML='<div class="mms-account-v7-title">Conta e aparência</div><div class="mms-account-v7-grid"><button data-x="blue"><span class="mms-swatch blue"></span><span>Azul</span></button><button data-x="pink"><span class="mms-swatch pink"></span><span>Rosa</span></button><button data-x="theme">☀︎ / ☾&nbsp; Tema</button><button data-x="logout" class="logout">Sair</button><button data-x="admin" class="admin full">Painel Admin</button></div>';
   list.appendChild(el);
   el.addEventListener('click',e=>{
    const b=e.target.closest('button[data-x]'); if(!b) return;
    const x=b.dataset.x;
    if(x==='blue') window.alterarCorPainel?.('azul');
    else if(x==='pink') window.alterarCorPainel?.('rosa');
    else if(x==='theme') window.alternarTema?.();
    else if(x==='logout') irParaLogin();
    else if(x==='admin'){
     root.classList.remove('is-open');
     document.documentElement.style.overflow='';
     window.alternarModo?.('admin');
    }
   });
  }
  el.style.display='block';
  el.style.visibility='visible';
  el.style.opacity='1';
 };

 const start=()=>{
  mount();
  setInterval(mount,500);
  new MutationObserver(mount).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style']});
 };
 if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();
</script>`;

    html = html.replace('</head>', css + '</head>').replace('</body>', js + '</body>');
    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.set('cache-control','no-store, max-age=0');
    return new Response(html,{status:response.status,statusText:response.statusText,headers});
  })());
});
