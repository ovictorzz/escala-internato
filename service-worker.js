const CACHE_VERSION = 't7a-push-v2';

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
    if (!html.includes('id="sw-mobile-controls-fix"')) {
      const css = `<style id="sw-mobile-controls-fix">
@media (max-width:1023px){
#mobile-nav-menu:not(.hidden){position:fixed!important;display:flex!important;flex-direction:column!important;top:calc(env(safe-area-inset-top) + 72px)!important;left:12px!important;right:12px!important;bottom:calc(env(safe-area-inset-bottom) + 82px)!important;z-index:130!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;padding:12px!important;border:1px solid rgba(148,163,184,.16)!important;border-radius:22px!important;background:rgba(8,10,18,.99)!important;box-shadow:0 28px 80px -20px rgba(0,0,0,.96)!important}
html:not(.dark) #mobile-nav-menu:not(.hidden){background:rgba(255,255,255,.99)!important}
#mobile-footer-menu.mobile-footer-inline{display:block!important;position:static!important;inset:auto!important;visibility:visible!important;opacity:1!important;max-height:none!important;overflow:visible!important;z-index:auto!important;margin-top:10px!important;padding:12px 0 0!important;border:0!important;border-top:1px solid rgba(148,163,184,.16)!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
#mobile-footer-menu.mobile-footer-inline #btn-header-admin{display:flex!important;visibility:visible!important;opacity:1!important}
#mobile-footer-menu.mobile-footer-inline button,#mobile-footer-menu.mobile-footer-inline a{pointer-events:auto!important}
}
</style>`;
      const js = `<script id="sw-mobile-controls-fix-script">
(()=>{
  const montarControlesMobile=()=>{
    if(window.innerWidth>=1024) return;
    const nav=document.getElementById('mobile-nav-menu');
    const footer=document.getElementById('mobile-footer-menu');
    if(!nav||!footer) return;
    if(footer.parentElement!==nav) nav.appendChild(footer);
    footer.classList.add('mobile-footer-inline');
  };
  const original=window.toggleMobileMenu;
  window.toggleMobileMenu=function(){
    montarControlesMobile();
    const nav=document.getElementById('mobile-nav-menu');
    const footer=document.getElementById('mobile-footer-menu');
    if(!nav||!footer){ if(typeof original==='function') return original(); return; }
    const abrindo=nav.classList.contains('hidden');
    nav.classList.toggle('hidden',!abrindo);
    footer.classList.toggle('hidden',!abrindo);
    footer.classList.add('mobile-footer-inline');
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',montarControlesMobile,{once:true});
  else montarControlesMobile();
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
