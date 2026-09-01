from pathlib import Path

p = Path('webauthn-browser.min.js')
s = p.read_text(encoding='utf-8')
marker = 'activity-trio-ranking-v2-20260901'

if marker not in s:
    patch = r'''

(()=>{
  const PATCH_ID='activity-trio-ranking-v2-20260901';
  if(window.__activityTrioRankingV2Patch===PATCH_ID) return;
  window.__activityTrioRankingV2Patch=PATCH_ID;

  const esc=(v)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));

  const style=document.createElement('style');
  style.id=PATCH_ID;
  style.textContent=`
    .atr2-shell{width:min(100%,1080px);margin:0 auto;display:flex;flex-direction:column;gap:14px}
    .atr2-consult-switch{width:min(100%,1080px);margin:0 auto 12px;display:flex;justify-content:flex-end}
    .atr2-switch{display:inline-flex;align-items:center;gap:3px;padding:4px;border:1px solid rgba(148,163,184,.11);border-radius:13px;background:rgba(7,9,16,.72)}
    .atr2-btn{height:36px;padding:0 13px;border:0;border-radius:9px;background:transparent;color:#71717a;font-family:'Outfit',sans-serif;font-size:10.5px;font-weight:800;white-space:nowrap;cursor:pointer}
    .atr2-btn.is-active{color:#eff6ff;background:linear-gradient(135deg,rgba(37,99,235,.26),rgba(79,70,229,.16));box-shadow:inset 0 0 0 1px rgba(96,165,250,.2)}

    .atr2-hero{position:relative;overflow:hidden;padding:18px 20px;border-radius:20px;border:1px solid rgba(96,165,250,.14);background:linear-gradient(145deg,rgba(15,20,34,.92),rgba(6,8,14,.92));box-shadow:0 22px 60px -44px rgba(37,99,235,.72)}
    .atr2-hero:before{content:'';position:absolute;inset:-90px auto auto -80px;width:260px;height:210px;background:radial-gradient(circle,rgba(59,130,246,.14),transparent 68%);pointer-events:none}
    .atr2-head{position:relative;display:flex;align-items:flex-start;justify-content:space-between;gap:18px}
    .atr2-kicker{color:#60a5fa;font-size:8.5px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}
    .atr2-title{margin-top:4px;color:#f8fafc;font-family:'Outfit',sans-serif;font-size:21px;line-height:1.05;font-weight:850;letter-spacing:-.03em}
    .atr2-subtitle{margin-top:5px;max-width:620px;color:#71717a;font-size:10.5px;line-height:1.45}
    .atr2-controls{position:relative;margin-top:15px;display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:10px;align-items:end}
    .atr2-field{min-width:0}
    .atr2-field label{display:block;margin:0 0 6px 2px;color:#71717a;font-size:8px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
    .atr2-select{width:100%;height:42px;padding:0 36px 0 12px;border-radius:12px;border:1px solid rgba(148,163,184,.14);outline:none;background:rgba(3,5,12,.76);color:#f4f4f5;font-family:'Outfit',sans-serif;font-size:11.5px;font-weight:720;box-shadow:none}
    .atr2-select:focus{border-color:rgba(59,130,246,.66);box-shadow:0 0 0 2px rgba(59,130,246,.12)}
    .atr2-summary{height:42px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;padding:0 12px;border-radius:12px;border:1px solid rgba(96,165,250,.11);background:rgba(59,130,246,.055)}
    .atr2-summary span{color:#60a5fa;font-size:7.5px;font-weight:900;letter-spacing:.13em;text-transform:uppercase}
    .atr2-summary strong{margin-top:2px;color:#f8fafc;font-family:'Outfit',sans-serif;font-size:13px;font-weight:850;line-height:1}

    .atr2-podium{width:min(100%,760px);margin:4px auto 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;align-items:end}
    .atr2-podium-card{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;min-width:0;padding:13px 7px 11px;border-radius:17px;border:1px solid rgba(148,163,184,.1);background:linear-gradient(160deg,rgba(17,20,31,.88),rgba(7,9,15,.8));text-align:center;overflow:hidden}
    .atr2-podium-card.first{min-height:145px;border-color:rgba(250,204,21,.22);background:linear-gradient(160deg,rgba(58,45,10,.22),rgba(8,10,17,.9));box-shadow:0 18px 42px -34px rgba(250,204,21,.88)}
    .atr2-podium-card.second{min-height:124px;border-color:rgba(203,213,225,.16)}
    .atr2-podium-card.third{min-height:112px;border-color:rgba(217,119,6,.17)}
    .atr2-medal{font-size:26px;line-height:1;filter:drop-shadow(0 7px 8px rgba(0,0,0,.28))}
    .atr2-place{margin-top:7px;color:#71717a;font-size:7px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
    .atr2-trio{margin-top:3px;color:#fff;font-family:'Outfit',sans-serif;font-size:14px;font-weight:850;white-space:nowrap}
    .atr2-count{margin-top:4px;color:#93c5fd;font-family:'Outfit',sans-serif;font-size:10.5px;font-weight:800}

    .atr2-list{width:min(100%,900px);margin:0 auto;display:flex;flex-direction:column;gap:6px}
    .atr2-row{display:grid;grid-template-columns:36px minmax(0,1fr) auto;align-items:center;gap:9px;min-height:48px;padding:0 12px;border-radius:14px;border:1px solid rgba(148,163,184,.085);background:linear-gradient(145deg,rgba(16,18,28,.62),rgba(7,9,15,.5))}
    .atr2-rank{width:27px;height:27px;display:grid;place-items:center;border-radius:9px;background:rgba(59,130,246,.075);color:#60a5fa;font-family:'Outfit',sans-serif;font-size:10px;font-weight:900}
    .atr2-row-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:12px;font-weight:800}
    .atr2-row-count{padding:5px 8px;border-radius:8px;background:rgba(255,255,255,.032);color:#a1a1aa;font-size:9px;font-weight:800;white-space:nowrap}
    .atr2-empty{width:min(100%,900px);margin:0 auto;padding:20px;border-radius:16px;border:1px solid rgba(148,163,184,.09);background:rgba(12,14,22,.55);color:#71717a;text-align:center;font-size:11px}

    html:not(.dark) .atr2-switch{background:#f8fafc;border-color:rgba(15,23,42,.08)}
    html:not(.dark) .atr2-btn{color:#64748b}
    html:not(.dark) .atr2-btn.is-active{color:#1d4ed8;background:rgba(59,130,246,.1)}
    html:not(.dark) .atr2-hero{background:linear-gradient(145deg,#fff,#f8fafc);border-color:rgba(59,130,246,.12)}
    html:not(.dark) .atr2-title,html:not(.dark) .atr2-trio,html:not(.dark) .atr2-summary strong,html:not(.dark) .atr2-row-trio{color:#0f172a}
    html:not(.dark) .atr2-select{background:#fff;color:#0f172a;border-color:rgba(15,23,42,.1)}
    html:not(.dark) .atr2-podium-card,html:not(.dark) .atr2-row,html:not(.dark) .atr2-empty{background:#fff;border-color:rgba(15,23,42,.08)}

    @media(max-width:700px){
      .atr2-shell{gap:11px}.atr2-consult-switch{justify-content:stretch}.atr2-switch{width:100%}.atr2-btn{flex:1;padding:0 8px;font-size:10px}
      .atr2-hero{padding:14px;border-radius:18px}.atr2-head{flex-direction:column;gap:10px}.atr2-head .atr2-switch{width:100%}.atr2-title{font-size:19px}.atr2-subtitle{font-size:10px}
      .atr2-controls{grid-template-columns:1fr;gap:8px}.atr2-select{height:42px}.atr2-summary{height:auto;min-height:42px}
      .atr2-podium{gap:6px}.atr2-podium-card{padding:11px 4px 9px;border-radius:14px}.atr2-podium-card.first{min-height:136px}.atr2-podium-card.second{min-height:118px}.atr2-podium-card.third{min-height:108px}
      .atr2-medal{font-size:23px}.atr2-trio{font-size:11.5px}.atr2-count{font-size:9.5px}.atr2-place{font-size:6.5px}
      .atr2-row{grid-template-columns:33px minmax(0,1fr) auto;min-height:46px;padding:0 10px}.atr2-row-trio{font-size:11px}.atr2-row-count{font-size:8.5px}
    }
  `;
  document.head.appendChild(style);

  const switchHtml=(ranking)=>`<div class="atr2-switch" role="tablist" aria-label="Modo da aba Atividades"><button class="atr2-btn ${ranking?'':'is-active'}" type="button" data-atr2-mode="consulta">Consultar escala</button><button class="atr2-btn ${ranking?'is-active':''}" type="button" data-atr2-mode="ranking">Ranking dos trios</button></div>`;

  const bindSwitch=(root)=>{
    root.querySelectorAll('[data-atr2-mode]').forEach(btn=>btn.addEventListener('click',()=>{
      window.__atividadeRankingAtivo=btn.dataset.atr2Mode==='ranking';
      window.renderizarFiltroAtividadeView?.();
    }));
  };

  const availableActivities=()=>{
    try{
      const lista=window.__obterAtividadesDisponiveis?.();
      return Array.isArray(lista)?lista.filter(Boolean):[];
    }catch(_){return [];}
  };

  const rankingFor=(atividade)=>{
    const counts=new Map(Array.from({length:10},(_,i)=>[String(i+1),0]));
    let ocorrencias=[];
    try{ocorrencias=window.__obterOcorrenciasAtividade?.(atividade)||[];}catch(_){ocorrencias=[];}
    ocorrencias.forEach(item=>{
      const id=String(item?.idTrio||'');
      if(counts.has(id)) counts.set(id,counts.get(id)+1);
    });
    const ranking=[...counts.entries()].map(([id,count])=>({id:Number(id),count}));
    ranking.sort((a,b)=>b.count-a.count||a.id-b.id);
    return {ranking,total:ocorrencias.length};
  };

  const renderRanking=()=>{
    const container=document.getElementById('lista-turnos');
    if(!container) return;
    const atividades=availableActivities();
    const preferida=window.__atividadeRankingLocal||window.atividadeSelecionadaGlobal||'';
    const atual=atividades.includes(preferida)?preferida:(atividades[0]||'');
    window.__atividadeRankingLocal=atual;
    const {ranking,total}=rankingFor(atual);
    const p1=ranking[0]||{id:1,count:0};
    const p2=ranking[1]||{id:2,count:0};
    const p3=ranking[2]||{id:3,count:0};
    const podium=(item,place,cls,medal)=>`<div class="atr2-podium-card ${cls}"><div class="atr2-medal">${medal}</div><div class="atr2-place">${place}º lugar</div><div class="atr2-trio">Trio ${String(item.id).padStart(2,'0')}</div><div class="atr2-count">${item.count} ${item.count===1?'vez':'vezes'}</div></div>`;
    const rows=ranking.slice(3).map((item,idx)=>`<div class="atr2-row"><div class="atr2-rank">${idx+4}º</div><div class="atr2-row-trio">Trio ${String(item.id).padStart(2,'0')}</div><div class="atr2-row-count">${item.count} ${item.count===1?'vez':'vezes'}</div></div>`).join('');
    const options=atividades.map(x=>`<option value="${esc(x)}" ${x===atual?'selected':''}>${esc(x)}</option>`).join('');

    container.innerHTML=`<div class="atr2-shell"><section class="atr2-hero"><div class="atr2-head"><div><div class="atr2-kicker">Comparativo por local</div><div class="atr2-title">Ranking dos trios</div><div class="atr2-subtitle">A mesma lista de atividades da consulta, agora comparando quantas vezes cada trio foi escalado em cada uma.</div></div>${switchHtml(true)}</div><div class="atr2-controls"><div class="atr2-field"><label for="atr2-ranking-local">Local ou atividade</label><select id="atr2-ranking-local" class="atr2-select">${options}</select></div><div class="atr2-summary"><span>Total registrado</span><strong>${total} ${total===1?'passagem':'passagens'}</strong></div></div></section>${atual?`<div class="atr2-podium">${podium(p2,2,'second','🥈')}${podium(p1,1,'first','🥇')}${podium(p3,3,'third','🥉')}</div><div class="atr2-list">${rows}</div>`:'<div class="atr2-empty">Nenhuma atividade disponível para o ranking.</div>'}</div>`;
    bindSwitch(container);
    const select=container.querySelector('#atr2-ranking-local');
    select?.addEventListener('change',()=>{window.__atividadeRankingLocal=select.value;renderRanking();});
  };

  const install=()=>{
    if(window.__atividadeRankingV2Installed) return true;
    if(!window.__atividadeRankingInstalado) return false;
    if(typeof window.__obterAtividadesDisponiveis!=='function'||typeof window.__obterOcorrenciasAtividade!=='function') return false;
    const baseOriginal=window.__atividadeRankingRenderOriginal||window.renderizarFiltroAtividadeView;
    if(typeof baseOriginal!=='function') return false;

    window.renderizarFiltroAtividadeView=function(){
      if(window.__atividadeRankingAtivo){renderRanking();return;}
      baseOriginal.apply(this,arguments);
      const container=document.getElementById('lista-turnos');
      if(!container) return;
      container.querySelectorAll('.atr-inline-switch,.atr2-consult-switch').forEach(el=>el.remove());
      const wrap=document.createElement('div');
      wrap.className='atr2-consult-switch';
      wrap.innerHTML=switchHtml(false);
      container.prepend(wrap);
      bindSwitch(wrap);
    };
    window.__atividadeRankingV2Installed=true;
    if(window.modoVisualizacao==='atividade') window.renderizarFiltroAtividadeView();
    return true;
  };

  if(!install()){
    let tries=0;
    const timer=setInterval(()=>{tries++;if(install()||tries>160) clearInterval(timer);},75);
  }
})();
'''
    s += patch
    p.write_text(s, encoding='utf-8')
