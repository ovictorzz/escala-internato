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

# Ranking v2: troca o número do trio pelos nomes dos integrantes.
tail = tail.replace(
    "Trio ${String(item.id).padStart(2,'0')}",
    "${esc(memberLabelRanking(item.id))}"
)

# Ajusta o texto para os nomes caberem bem no pódio e na lista, inclusive no mobile.
tail = tail.replace(
    ".atr2-trio{margin-top:3px;color:#fff;font-family:'Outfit',sans-serif;font-size:14px;font-weight:850;white-space:nowrap}",
    ".atr2-trio{margin-top:5px;color:#fff;font-family:'Outfit',sans-serif;font-size:12px;font-weight:850;line-height:1.17;text-align:center;white-space:normal;overflow-wrap:anywhere;max-width:100%}",
    1,
)
tail = tail.replace(
    ".atr2-row-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:12px;font-weight:800}",
    ".atr2-row-trio{color:#e4e4e7;font-family:'Outfit',sans-serif;font-size:11.5px;font-weight:800;line-height:1.24;min-width:0}",
    1,
)
tail = tail.replace(
    ".atr2-medal{font-size:23px}.atr2-trio{font-size:11.5px}.atr2-count{font-size:9.5px}.atr2-place{font-size:6.5px}",
    ".atr2-medal{font-size:23px}.atr2-trio{font-size:9.5px;line-height:1.14}.atr2-count{font-size:9.5px}.atr2-place{font-size:6.5px}",
    1,
)
tail = tail.replace(
    ".atr2-row{grid-template-columns:33px minmax(0,1fr) auto;min-height:46px;padding:0 10px}.atr2-row-trio{font-size:11px}.atr2-row-count{font-size:8.5px}",
    ".atr2-row{grid-template-columns:33px minmax(0,1fr) auto;min-height:52px;padding:6px 10px}.atr2-row-trio{font-size:10px;line-height:1.2}.atr2-row-count{font-size:8.5px}",
    1,
)

s = head + marker + tail
p.write_text(s, encoding='utf-8')
