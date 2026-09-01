from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove o loader intermediário do wrapper. A tela oficial do app continua sendo exibida
# normalmente depois que base-index.html é carregado. Em caso de erro, o catch ainda
# torna #boot visível e mostra a mensagem de falha.
s = s.replace(
    '#boot{display:grid;min-height:100vh;min-height:100dvh;place-items:center;padding:24px;text-align:center}',
    '#boot{display:none;min-height:100vh;min-height:100dvh;place-items:center;padding:24px;text-align:center}',
    1,
)
s = s.replace(
    '<div id="boot"><div class="boot-card">Carregando Painel T7A…</div></div>',
    '<div id="boot" aria-hidden="true"></div>',
    1,
)

# Expõe apenas os helpers já existentes da aba Atividades para patches de UI externos.
# A inserção acontece no HTML carregado, dentro do mesmo escopo em que as funções existem.
helper_marker = 'window.__obterAtividadesDisponiveis = obterAtividadesDisponiveis;'
if helper_marker not in s:
    needle = '    document.open();'
    if needle not in s:
        raise SystemExit('document.open anchor not found')
    injection = '''    const activityHelpersAnchor='window.renderizarFiltroAtividadeView = function() {';
    if (html.includes(activityHelpersAnchor) && !html.includes('window.__obterAtividadesDisponiveis = obterAtividadesDisponiveis;')) {
      html=html.replace(activityHelpersAnchor,`window.__obterAtividadesDisponiveis = obterAtividadesDisponiveis;
window.__obterOcorrenciasAtividade = obterOcorrenciasAtividade;
${activityHelpersAnchor}`);
    }

'''
    s = s.replace(needle, injection + needle, 1)

if 'Carregando Painel T7A…' in s:
    raise SystemExit('Intermediate loader text still present')
if helper_marker not in s:
    raise SystemExit('Activity helpers exposure missing')

p.write_text(s, encoding='utf-8')
