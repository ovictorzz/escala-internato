from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '    document.open();'
if 'direct-faceid-menu-fix-v2' in s:
    raise SystemExit(0)

inject = r'''    const directFaceIdMenuFix = `<script id="direct-faceid-menu-fix-v2">
(()=>{
  const ensureFaceId=()=>{
    if(innerWidth>=1024) return;
    const root=document.getElementById('mobile-menu-stable');
    if(!root) return;
    const account=root.querySelector('[class*="mms-account-v"]');
    const grid=account?.querySelector('[class*="-grid"]');
    if(!grid || grid.querySelector('[data-direct-faceid="1"]')) return;
    const btn=document.createElement('button');
    btn.type='button';
    btn.dataset.directFaceid='1';
    btn.className='faceid full';
    btn.style.cssText='grid-column:1/-1;min-height:52px;display:flex;align-items:center;justify-content:center;gap:9px;border-radius:13px;border:1px solid rgba(56,189,248,.28);background:linear-gradient(135deg,rgba(14,165,233,.14),rgba(59,130,246,.09));color:#7dd3fc;font:750 12px/1.1 Outfit,sans-serif;padding:8px';
    btn.innerHTML='<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 3H6a3 3 0 00-3 3v2m13-5h2a3 3 0 013 3v2M8 21H6a3 3 0 01-3-3v-2m13 5h2a3 3 0 003-3v-2M9 10h.01M15 10h.01M9 15c1.7 1.35 4.3 1.35 6 0"/></svg><span>Cadastrar Face ID neste aparelho</span>';
    const admin=grid.querySelector('[data-x="admin"], .admin');
    if(admin) grid.insertBefore(btn,admin); else grid.appendChild(btn);
    btn.addEventListener('click',()=>{
      root.classList.remove('is-open');
      document.documentElement.style.overflow='';
      if(typeof window.abrirConfiguracaoFaceID==='function') window.abrirConfiguracaoFaceID();
      else document.getElementById('faceid-setup-button')?.click();
    });
  };
  const start=()=>{
    ensureFaceId();
    setInterval(ensureFaceId,300);
    new MutationObserver(ensureFaceId).observe(document.documentElement,{childList:true,subtree:true});
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();
<\/script>`;
    html=html.replace('</body>',directFaceIdMenuFix+'</body>');

'''

if marker not in s:
    raise SystemExit('marker not found')
p.write_text(s.replace(marker, inject + marker, 1), encoding='utf-8')
