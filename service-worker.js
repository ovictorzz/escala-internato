const CACHE_VERSION = 't7a-push-v1';

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
    try {
      data = { body: event.data ? event.data.text() : '' };
    } catch (_) {
      data = {};
    }
  }

  const title = data.title || 'Painel T7A';
  const options = {
    body: data.body || data.message || 'Você tem uma nova atualização.',
    icon: data.icon || '/apple-touch-icon.png',
    badge: data.badge || '/apple-touch-icon.png',
    data: {
      url: data.url || data.link || '/',
      ...((data.data && typeof data.data === 'object') ? data.data : {})
    },
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
        try {
          if ('navigate' in client) await client.navigate(targetUrl);
        } catch (_) {}
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
    const marker = 'id="sw-mobile-footer-fix"';
    if (!html.includes(marker)) {
      const css = `<style id="sw-mobile-footer-fix">
@media (max-width:1023px){
#mobile-footer-menu:not(.hidden){display:block!important;visibility:visible!important;opacity:1!important;position:fixed!important;left:12px!important;right:12px!important;bottom:calc(env(safe-area-inset-bottom) + 82px)!important;max-height:min(220px,32dvh)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;z-index:130!important;padding:12px!important;background:rgba(8,10,18,.99)!important;border:1px solid rgba(148,163,184,.18)!important;border-radius:18px!important;box-shadow:0 24px 70px -24px rgba(0,0,0,.96)!important;backdrop-filter:blur(24px) saturate(135%)!important;-webkit-backdrop-filter:blur(24px) saturate(135%)!important}
html:not(.dark) #mobile-footer-menu:not(.hidden){background:rgba(255,255,255,.99)!important}
#mobile-nav-menu:not(.hidden){bottom:calc(env(safe-area-inset-bottom) + 320px)!important;z-index:125!important}
#mobile-footer-menu:not(.hidden) button,#mobile-footer-menu:not(.hidden) a{pointer-events:auto!important}
#btn-header-admin{display:flex!important}
}
</style>`;
      html = html.replace('</head>', `${css}</head>`);
    }

    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.set('cache-control', 'no-store');
    return new Response(html, { status: response.status, statusText: response.statusText, headers });
  })());
});
