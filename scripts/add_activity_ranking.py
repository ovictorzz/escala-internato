from pathlib import Path

p = Path('webauthn-browser.min.js')
s = p.read_text(encoding='utf-8')
marker = 'activity-trio-ranking-20260901'

if marker not in s:
    patch = r'''

(()=>{
  const PATCH_ID='activity-trio-ranking-20260901';
  if(window.__activityTrioRankingPatch===PATCH_ID) return;
  window.__activityTrioRankingPatch=PATCH_ID;

  const norm=(v)=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\s+/g,' ').trim().toLowerCase();
  const esc=(v)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const isClinical=(local)=>{
    const t=norm(local);
    if(!t||t==='—'||t==='-'||t==='livre') return false;
    if(t.includes('seminario')||t.includes('simulado')||t.includes('avaliacao somativa')||t.includes('sessoes clinicas integradas')||t.includes('aula teorica')) return false;
    if(t==='sci'||t.startsWith('sci ')) return false;
    return true;
  };

  const style=document.createElement('style');
  style.id=PATCH_ID;
  style.textContent=`
  .atr-mode-switch{display:inline-grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;border:1px solid rgba(148,163,184,.12);border-radius:14px;background:rgba(9,11,20,.72);box-shadow:inset 0 1px 0 rgba(255,255,255,.025)}
  .atr-mode-btn{min-height:38px;padding:0 14px;border:0;border-radius:10px;background:transparent;color:#71717a;font-family:'Outfit',sans-serif;font-size:11px;font-weight:800;letter-spacing:.01em;white-space:nowrap;cursor:pointer}
  .atr-mode-btn.is-active{color:#eff6ff;background:linear-gradient(135deg,rgba(37,99,235,.28),rgba(79,70,229,.18));box-shadow:inset 0 0 0 1px rgba(96,165,250,.22),0 8px 24px -18px rgba(59,130,246,.8)}
  .atr-ranking-shell{display:flex;flex-direction:column;gap:14px}
  .atr-ranking-hero{position:relative;overflow:hidden;padding:18px;border-radius:22px;border:1px solid rgba(96,165,250,.16);background:linear-gradient(145deg,rgba(17,22,37,.9),rgba(7,9,16,.9));box-shadow:0 22px 60px -40px rgba(37,99,235,.72)}
  .atr-ranking-hero:before{content:'';position:absolute;inset:-80px auto auto -60px;width:220px;height:180px;background:radial-gradient(circle,rgba(59,130,246,.17),transparent 68%);pointer-events:none}
  .atr-kicker{position:relative;color:#60a5fa;font-size:9px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}
  .atr-title{position:relative;margin-top:5px;color:#f8fafc;font-family:'Outfit',sans-serif;font-size:22px;font-weight:850;letter-spacing:-.03em}
  .atr-subtitle{position:relative;margin-top:4px;color:#71717a;font-size:11px;line-height:1.45}
  .atr-hero-row{position:relative;margin-top:14px;display:flex;align-items:end;justify-content:space-between;gap:12px;flex-wrap:wrap}
  .atr-field{flex:1 1 320px;min-width:0}
  .atr-field label{display:block;margin:0 0 6px 2px;color:#71717a;font-size:9px;font-weight:850;letter-spacing:.13em;text-transform:uppercase}
  .atr-select{width:100%;min-height:46px;padding:0 40px 0 13px;border-radius:13px;border:1px solid rgba(148,163,184,.15);outline:none;background:rgba(3,5,12,.72);color:#f4f4f5;font-family:'Outfit',sans-serif;font-size:12px;font-weight:720}
  .atr-summary{flex:0 0 auto;min-width:142px;padding:10px 12px;border-radius:13px;border:1px solid rgba(96,165,250,.12);background:rgba(59,130,246,.065)}
  .atr-summary span{display:block;color:#60a5fa;font-size:8px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
  .atr-summary strong{display:block;margin-top:3px;color:#f8fafc;font-family:'Outfit',sans-serif;font-size:15px;font-weight:850}
  .atr-podium{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:end;padding:8px 0 2px}
  .atr-podium-card{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;min-width:0;padding:15px 8px 12px;border-radius:18px;border:1px solid rgba(148,163,184,.11);background:linear-gradient(160deg,rgba(18,20,31,.9),rgba(7,9,16,.82));text-align:center;overflow:hidden}
  .atr-podium-card.first{min-height:162px;border-color:rgba(250,204,21,.24);background:linear-gradient(160deg,rgba(51,41,14,.24),rgba(8,10,17,.9));box-shadow:0 20px 45px -35px rgba(250,204,21,.9)}
  .atr-podium-card.second{min-height:138px;border-color:rgba(203,213,225,.18)}
  .atr-podium-card.third{min-height:124px;border-color:rgba(217,119,6,.18)}
  .atr-medal{font-size:28px;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.3))}
  .atr-place{margin-top:8px;color:#71717a;font-size:8px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
  .atr-trio{margin-top:3px;color:#fff;font-family:'Outfit',sans-serif;font-size:15px;font-weight:850;white-space:nowrap}
  .atr-count{margin-top:5px;color:#93c5fd;font-family:'Outfit',sans-serif;font-size:12px;font-weight:800}
  .atr-ranking-list{display:flex;flex-direction:column;gap:7px}
  .atr-rank-row{display:grid;grid-template-columns:40px minmax(0,1fr) auto;align-items:center;gap:10px;min-height:54px;padding:0 13px;border-radius:15px;border:1px solid rgba(148,163,184,.09);background:linear-gradient(145deg,rgba(17,19,29,.66),rgba(7,9,15,.55))}
  .atr-rank-number{width:30px;height:30px;display:grid;place-items:center;border-radius:10px;background:rgba(59,130,246,.08);color:#60a5fa;font-family:'Outfit',sans-serif;font-size:11px;font-weight:900}
  .atr-rank-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:13px;font-weight:800}
  .atr-rank-count{padding:6px 9px;border-radius:9px;background:rgba(255,255,255,.035);color:#a1a1aa;font-size:10px;font-weight:800;white-space:nowrap}
  .atr-inline-switch{display:flex;justify-content:flex-end;margin:0 0 12px}
  html:not(.dark) .atr-mode-switch{background:rgba(248,250,252,.9);border-color:rgba(15,23,42,.08)}
  html:not(.dark) .atr-mode-btn{color:#64748b}
  html:not(.dark) .atr-mode-btn.is-active{color:#1d4ed8;background:rgba(59,130,246,.1)}
  html:not(.dark) .atr-ranking-hero{background:linear-gradient(145deg,#fff,#f8fafc);border-color:rgba(59,130,246,.13)}
  html:not(.dark) .atr-title,html:not(.dark) .atr-podium-card .atr-trio{color:#0f172a}
  html:not(.dark) .atr-select{background:#fff;color:#0f172a;border-color:rgba(15,23,42,.1)}
  html:not(.dark) .atr-summary{background:rgba(59,130,246,.06)}
  html:not(.dark) .atr-summary strong{color:#0f172a}
  html:not(.dark) .atr-podium-card,html:not(.dark) .atr-rank-row{background:#fff;border-color:rgba(15,23,42,.08)}
  html:not(.dark) .atr-rank-trio{color:#0f172a}
  @media(max-width:640px){
    .atr-inline-switch{justify-content:stretch}.atr-mode-switch{width:100%}.atr-mode-btn{padding:0 8px;font-size:10px}
    .atr-ranking-hero{padding:14px;border-radius:18px}.atr-title{font-size:19px}.atr-hero-row{align-items:stretch}.atr-summary{width:100%;box-sizing:border-box}
    .atr-podium{gap:6px}.atr-podium-card{padding:12px 4px 10px;border-radius:15px}.atr-podium-card.first{min-height:148px}.atr-podium-card.second{min-height:126px}.atr-podium-card.third{min-height:114px}
    .atr-medal{font-size:24px}.atr-trio{font-size:12px}.atr-count{font-size:10px}.atr-place{font-size:7px}
    .atr-rank-row{grid-template-columns:36px minmax(0,1fr) auto;min-height:50px;padding:0 10px}.atr-rank-trio{font-size:12px}.atr-rank-count{font-size:9px}
  }
  `;
  document.head.appendChild(style);

  const allClinicalLocations=()=>{
    const labels=new Map();
    try{
      for(let id=1;id<=10;id++){
        const semanas=dadosEscala?.[id]?.semanas||{};
        Object.values(semanas).forEach(sem=>Object.values(sem||{}).forEach(dia=>(dia?.turnos||[]).forEach(turno=>{
          const local=String(turno?.local||'').trim();
          if(!isClinical(local)) return;
          const key=norm(local);
          if(!labels.has(key)) labels.set(key,local);
        })));
      }
    }catch(_){return [];}
    return [...labels.values()].sort((a,b)=>a.localeCompare(b,'pt-BR',{sensitivity:'base'}));
  };

  const rankingFor=(local)=>{
    const key=norm(local);
    const ranking=[];
    for(let id=1;id<=10;id++){
      let count=0;
      try{
        const semanas=dadosEscala?.[id]?.semanas||{};
        Object.values(semanas).forEach(sem=>Object.values(sem||{}).forEach(dia=>(dia?.turnos||[]).forEach(turno=>{
          if(norm(turno?.local)===key) count++;
        })));
      }catch(_){}
      ranking.push({id,count});
    }
    ranking.sort((a,b)=>b.count-a.count||a.id-b.id);
    return ranking;
  };

  const switchHtml=(ranking)=>`<div class="atr-mode-switch" role="tablist" aria-label="Modo da aba Atividades"><button class="atr-mode-btn ${ranking?'':'is-active'}" type="button" data-atr-mode="consulta">Consultar escala</button><button class="atr-mode-btn ${ranking?'is-active':''}" type="button" data-atr-mode="ranking">Ranking dos trios</button></div>`;

  const bindSwitch=(root)=>{
    root.querySelectorAll('[data-atr-mode]').forEach(btn=>btn.addEventListener('click',()=>{
      window.__atividadeRankingAtivo=btn.dataset.atrMode==='ranking';
      window.renderizarFiltroAtividadeView?.();
    }));
  };

  const renderRanking=()=>{
    const container=document.getElementById('lista-turnos');
    if(!container) return;
    const locais=allClinicalLocations();
    const atual=locais.includes(window.__atividadeRankingLocal)?window.__atividadeRankingLocal:(locais[0]||'');
    window.__atividadeRankingLocal=atual;
    const ranking=rankingFor(atual);
    const total=ranking.reduce((s,x)=>s+x.count,0);
    const p1=ranking[0]||{id:1,count:0},p2=ranking[1]||{id:2,count:0},p3=ranking[2]||{id:3,count:0};
    const podiumCard=(item,place,cls,medal)=>`<div class="atr-podium-card ${cls}"><div class="atr-medal">${medal}</div><div class="atr-place">${place}º lugar</div><div class="atr-trio">Trio ${String(item.id).padStart(2,'0')}</div><div class="atr-count">${item.count} ${item.count===1?'vez':'vezes'}</div></div>`;
    const rows=ranking.slice(3).map((item,idx)=>`<div class="atr-rank-row"><div class="atr-rank-number">${idx+4}º</div><div class="atr-rank-trio">Trio ${String(item.id).padStart(2,'0')}</div><div class="atr-rank-count">${item.count} ${item.count===1?'vez':'vezes'}</div></div>`).join('');
    const options=locais.map(x=>`<option value="${esc(x)}" ${x===atual?'selected':''}>${esc(x)}</option>`).join('');

    container.innerHTML=`<div class="atr-ranking-shell"><div class="atr-inline-switch">${switchHtml(true)}</div><section class="atr-ranking-hero"><div class="atr-kicker">Comparativo por local</div><div class="atr-title">Ranking dos trios</div><div class="atr-subtitle">Veja quantas vezes cada trio já foi escalado em cada local/atividade clínica.</div><div class="atr-hero-row"><div class="atr-field"><label for="atr-ranking-local">Local ou atividade</label><select id="atr-ranking-local" class="atr-select">${options}</select></div><div class="atr-summary"><span>Total registrado</span><strong>${total} ${total===1?'passagem':'passagens'}</strong></div></div></section>${atual?`<div class="atr-podium">${podiumCard(p2,2,'second','🥈')}${podiumCard(p1,1,'first','🥇')}${podiumCard(p3,3,'third','🥉')}</div><div class="atr-ranking-list">${rows}</div>`:'<div class="glass-panel rounded-2xl p-6 text-center text-sm text-zinc-500">Nenhum local clínico disponível para o ranking.</div>'}</div>`;
    bindSwitch(container);
    const select=container.querySelector('#atr-ranking-local');
    select?.addEventListener('change',()=>{window.__atividadeRankingLocal=select.value;renderRanking();});
  };

  const install=()=>{
    if(window.__atividadeRankingInstalado) return true;
    if(typeof window.renderizarFiltroAtividadeView!=='function') return false;
    const original=window.renderizarFiltroAtividadeView;
    window.__atividadeRankingRenderOriginal=original;
    window.renderizarFiltroAtividadeView=function(){
      if(window.__atividadeRankingAtivo){renderRanking();return;}
      original.apply(this,arguments);
      const container=document.getElementById('lista-turnos');
      if(!container||container.querySelector('.atr-inline-switch')) return;
      const wrap=document.createElement('div');
      wrap.className='atr-inline-switch';
      wrap.innerHTML=switchHtml(false);
      container.prepend(wrap);
      bindSwitch(wrap);
    };
    window.__atividadeRankingInstalado=true;
    if(window.modoVisualizacao==='atividade') window.renderizarFiltroAtividadeView();
    return true;
  };

  const start=()=>{
    if(install()) return;
    let tentativas=0;
    const timer=setInterval(()=>{tentativas++;if(install()||tentativas>80)clearInterval(timer);},100);
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();
'''
    s += patch
    p.write_text(s, encoding='utf-8')
