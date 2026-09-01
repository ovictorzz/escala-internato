from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old_decl = '    const directFaceIdMenuFix = `<script id="direct-faceid-menu-fix-v2">'
new_decl = '    const directFaceIdMenuFixV2 = `<script id="direct-faceid-menu-fix-v2">'
if old_decl in s:
    before, after = s.split(old_decl, 1)
    after = after.replace("html=html.replace('</body>',directFaceIdMenuFix+'</body>');", "html=html.replace('</body>',directFaceIdMenuFixV2+'</body>');", 1)
    s = before + new_decl + after

# Evita tela totalmente preta se algum erro futuro ocorrer antes do loader terminar.
s = s.replace('#boot{display:none;', '#boot{display:grid;', 1)
s = s.replace('<div id="boot"><div class="boot-card"></div></div>', '<div id="boot"><div class="boot-card">Carregando Painel T7A…</div></div>', 1)

p.write_text(s, encoding='utf-8')
