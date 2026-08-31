from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = s.find('    const directFaceIdMenuFix = `')
end_marker = "    html=html.replace('</body>',directFaceIdMenuFix+'</body>');"
end = s.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit('direct patch block not found')
end += len(end_marker)

block = r'''    const directFaceIdMenuFix = `<script id="direct-account-menu-fix-v3">
(()=>{
  const closeMenu=(root)=>{root?.classList.remove('is-open');document.documentElement.style.overflow='';};
  const logout=()=>{
    try{sessionStorage.removeItem('autenticado');sessionStorage.removeItem('alunoLogado');sessionStorage.removeItem('adminAutenticado');}catch(_){}
    document.body.classList.remove('app-authenticated');
    const login=document.getElementById('login-overlay');
    if(login){login.style.display='flex';login.classList.remove('hidden');login.style.visibility='visible';login.style.opacity='1';}
    else location.replace('/');
  };
  const ensure=()=>{
    if(innerWidth>=1024)return;
    const root=document.getElementById('mobile-menu-stable');
    const list=root?.querySelector('.mms-list');
    if(!root||!list)return;
    root.querySelectorAll('[class*="mms-account-v"],[data-account-section]').forEach(n=>n.remove());
    const section=document.createElement('div');
    section.dataset.accountSection='v3';
    section.style.cssText='display:block!important;visibility:visible!important;opacity:1!important;margin-top:8px;padding:11px 2px 2px;border-top:1px solid rgba(148,163,184,.13)';
    section.innerHTML='<div style="padding:0 7px 9px;font:800 9px/1 Outfit,sans-serif;letter-spacing:.15em;text-transform:uppercase;color:#71717a">Conta e aparência</div><div data-account-grid="v3" style="display:grid;grid-template-columns:1fr 1fr;gap:7px"><button data-x="blue" style="min-height:47px;border-radius:13px;border:1px solid rgba(148,163,184,.13);background:rgba(255,255,255,.04);color:#e4e4e7;font:750 12px/1.1 Outfit,sans-serif;padding:8px;display:flex;align-items:center;justify-content:center;gap:9px"><span style="width:20px;height:20px;border-radius:50%;background:#3b82f6;border:2px solid rgba(255,255,255,.75)"></span>Azul</button><button data-x="pink" style="min-height:47px;border-radius:13px;border:1px solid rgba(148,163,184,.13);background:rgba(255,255,255,.04);color:#e4e4e7;font:750 12px/1.1 Outfit,sans-serif;padding:8px;display:flex;align-items:center;justify-content:center;gap:9px"><span style="width:20px;height:20px;border-radius:50%;background:#ec4899;border:2px solid rgba(255,255,255,.75)"></span>Rosa</button><button data-x="theme" style="min-height:47px;border-radius:13px;border:1px solid rgba(148,163,184,.13);background:rgba(255,255,255,.04);color:#e4e4e7;font:750 12px/1.1 Outfit,sans-serif;padding:8px">☀︎ / ☾ Tema</button><button data-x="logout" style="min-height:47px;border-radius:13px;border:1px solid rgba(244,63,94,.18);background:rgba(244,63,94,.08);color:#fb7185;font:750 12px/1.1 Outfit,sans-serif;padding:8px">Sair</button><button data-x="faceid" style="grid-column:1/-1;min-height:52px;border-radius:13px;border:1px solid rgba(56,189,248,.28);background:linear-gradient(135deg,rgba(14,165,233,.14),rgba(59,130,246,.09));color:#7dd3fc;font:750 12px/1.1 Outfit,sans-serif;padding:8px">Cadastrar Face ID neste aparelho</button><button data-x="admin" style="grid-column:1/-1;min-height:47px;border-radius:13px;border:1px solid rgba(99,102,241,.24);background:rgba(79,70,229,.12);color:#a5b4fc;font:750 12px/1.1 Outfit,sans-serif;padding:8px">Painel Admin</button></div>';
    list.appendChild(section);
    section.addEventListener('click',e=>{
      const b=e.target.closest('button[data-x]');if(!b)return;const x=b.dataset.x;
      if(x==='blue')window.alterarCorPainel?.('azul');
      else if(x==='pink')window.alterarCorPainel?.('rosa');
      else if(x==='theme')window.alternarTema?.();
      else if(x==='logout'){closeMenu(root);logout();}
      else if(x==='faceid'){closeMenu(root);if(typeof window.abrirConfiguracaoFaceID==='function')window.abrirConfiguracaoFaceID();else document.getElementById('faceid-setup-button')?.click();}
      else if(x==='admin'){closeMenu(root);window.alternarModo?.('admin');}
    });
  };
  const start=()=>{ensure();setInterval(()=>{if(!document.querySelector('#mobile-menu-stable [data-account-section="v3"]'))ensure();},300);new MutationObserver(()=>{if(!document.querySelector('#mobile-menu-stable [data-account-section="v3"]'))ensure();}).observe(document.documentElement,{childList:true,subtree:true});};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
<\/script>`;
    html=html.replace('</body>',directFaceIdMenuFix+'</body>');'''

p.write_text(s[:start] + block + s[end:], encoding='utf-8')
