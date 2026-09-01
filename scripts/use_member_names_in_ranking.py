from pathlib import Path

p = Path('webauthn-browser.min.js')
s = p.read_text(encoding='utf-8')
marker = "activity-trio-ranking-v2-20260901"
if marker not in s:
    raise SystemExit('Ranking v2 marker not found')

head, tail = s.split(marker, 1)

if 'const memberNamesRanking=' not in tail:
    anchor = "  const renderRanking=()=>{"
    if anchor not in tail:
        raise SystemExit('renderRanking anchor not found')
    mapping = """  const memberNamesRanking={
    1:'André, Davi & Letícia B.',
    2:'Nadya, Louise & Isabella T.',
    3:'Hiago, Isabela & Mª Eduarda Aquino',
    4:'Heitor, Bruno & Andressa M.',
    5:'Mª Luiza, Mª Eduarda Santiago & Luiza de S.',
    6:'Leticia M., Júlia & Luiza B.',
    7:'Ana Clara, Carolina B. & Kamilly',
    8:'Giovanna, Rayane & Sofia',
    9:'Annelise, Camila S. & Gabriella',
    10:'José, João Victor & Ana Luiza'
  };
  const memberLabelRanking=(id)=>memberNamesRanking[Number(id)]||`Trio ${String(id).padStart(2,'0')}`;

"""
    tail = tail.replace(anchor, mapping + anchor, 1)

old_podium = '<div class=\\"atr-trio\\">Trio ${String(item.id).padStart(2,\'0\')}</div>'
new_podium = '<div class=\\"atr-trio\\">${esc(memberLabelRanking(item.id))}</div>'
old_row = '<div class=\\"atr-rank-trio\\">Trio ${String(item.id).padStart(2,\'0\')}</div>'
new_row = '<div class=\\"atr-rank-trio\\">${esc(memberLabelRanking(item.id))}</div>'

tail = tail.replace(old_podium, new_podium)
tail = tail.replace(old_row, new_row)

tail = tail.replace(
    ".atr-trio{margin-top:3px;color:#fff;font-family:'Outfit',sans-serif;font-size:15px;font-weight:850;white-space:nowrap}",
    ".atr-trio{margin-top:5px;color:#fff;font-family:'Outfit',sans-serif;font-size:13px;font-weight:850;line-height:1.18;text-align:center;white-space:normal;overflow-wrap:anywhere;max-width:100%}",
    1,
)
tail = tail.replace(
    ".atr-rank-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:13px;font-weight:800}",
    ".atr-rank-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:12px;font-weight:800;line-height:1.25;min-width:0}",
    1,
)
tail = tail.replace(
    ".atr-medal{font-size:24px}.atr-trio{font-size:12px}.atr-count{font-size:10px}.atr-place{font-size:7px}",
    ".atr-medal{font-size:24px}.atr-trio{font-size:10.5px;line-height:1.15}.atr-count{font-size:10px}.atr-place{font-size:7px}",
    1,
)
tail = tail.replace(
    ".atr-rank-row{grid-template-columns:36px minmax(0,1fr) auto;min-height:50px;padding:0 10px}.atr-rank-trio{font-size:12px}.atr-rank-count{font-size:9px}",
    ".atr-rank-row{grid-template-columns:36px minmax(0,1fr) auto;min-height:54px;padding:7px 10px}.atr-rank-trio{font-size:10.5px}.atr-rank-count{font-size:9px}",
    1,
)

s = head + marker + tail
p.write_text(s, encoding='utf-8')
